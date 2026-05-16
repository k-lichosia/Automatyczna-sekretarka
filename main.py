import os
import json
import imaplib
import smtplib
import email
import email.utils
import locale
from langdetect import detect
from dotenv import load_dotenv 
from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

load_dotenv() 
LOG_FILE = "replied_emails.txt"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com" #fill with correct data (np. "imap.poczta.onet.pl" for Onet mailbox)
SMTP_SERVER = "smtp.gmail.com" #fill with correct data (np. "smtp.poczta.onet.pl" dla Onet mailbox)

def wczytaj_tlumaczenia():
    with open('replies.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def czy_juz_odpowiedziano(email):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, "r") as f:
        wyslane = set(f.read().splitlines())
    return email in wyslane

def zapisz_wyslanego_maila(email):
    with open(LOG_FILE, "a") as f:
        f.write(email + "\n")

def dekoduj_naglowek(text):
    if not text:
        return ""
    decoded, encoding = decode_header(text)[0]
    if isinstance(decoded, bytes):
        return decoded.decode(encoding if encoding else 'utf-8')
    return decoded

def sprawdz_i_odpowiedz():
    try:
        try:
            locale.setlocale(locale.LC_TIME, 'C')
        except:
            pass

        SZABLONY = wczytaj_tlumaczenia()
        print("Łączenie ze skrzynką...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        dzisiaj = datetime.now().strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'UNSEEN SINCE {dzisiaj}')

        if not messages[0]:
            print("Brak nowych wiadomości.")
            return

        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = dekoduj_naglowek(msg["Subject"])
            full_sender = msg["From"]
            _, sender_email = email.utils.parseaddr(full_sender)
            
            print(f"Przetwarzanie: {subject} od {sender_email}")

            slowa_klucze = [
                "namiot", "pole", "kemping", "camper", "przyczepa", "namioty", "kamper", "pole namiotowe",
                "tent", "camping", "pitch", "campsite", "caravan", "motorhome", "campervan",
                "zelt", "campingplatz", "wohnwagen", "wohnmobil", "stellplatz", "zelten",
                "stan", "kemp", "karavan", "obytný vůz", "stanování", "přívěs"
            ]
            tresc_maila = ""
            
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            tresc_maila += payload.decode(errors='ignore')
            else:
                tresc_maila = msg.get_payload(decode=True).decode(errors='ignore')

            calosc_tekstu = (subject + " " + tresc_maila).lower()

            try:
                jezyk = detect(calosc_tekstu) 
                if jezyk not in SZABLONY:
                    jezyk = 'en' 
            except:
                jezyk = 'pl'

            szablon = SZABLONY[jezyk]
            
            if any(s in calosc_tekstu for s in slowa_klucze):
                temat = szablon['temat_pole']
                tresc = szablon['tresc_pole']
                kategoria = f"POLE_{jezyk.upper()}"
            else:
                temat = szablon['temat_ogolny']
                tresc = szablon['tresc_ogolna']
                kategoria = f"OGOLNE_{jezyk.upper()}"

            klucz = f"{sender_email}|{kategoria}"
            if not czy_juz_odpowiedziano(klucz):
                print(f"!!! Wysyłam {kategoria} do: {sender_email}")
                wyslij_odpowiedz(sender_email, temat, tresc)
                zapisz_wyslanego_maila(klucz)
            else:
                print(f"Ignoruje: {sender_email} już otrzymał dzisiaj {kategoria}.")

        mail.logout()
        
    except Exception as e:
        print(f"Błąd: {e}")

def wyslij_odpowiedz(odbiorca, temat, tresc):
    try:
        msg = MIMEMultipart() 
        msg['From'] = EMAIL_USER 
        msg['To'] = odbiorca 
        msg['Subject'] = temat

        msg.attach(MIMEText(tresc, 'plain', 'utf-8'))

        with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        
        print(f"Wysłano: {temat} do {odbiorca}")
        
    except Exception as e:
        print(f"Błąd podczas wysyłania: {e}")

if __name__ == "__main__":
    sprawdz_i_odpowiedz()
