# Automatyczna sekretarka dla kempingu 

### Inteligentny asystent e-mailowy z detekcją języka i systemem anty-spam.

## O projekcie
Projekt powstał z myślą o optymalizacji pracy recepcji kempingowej. Program automatyzuje obsługę zapytań e-mailowych, odciążając pracowników od odpowiadania na powtarzające się pytania (np. o dostępność pola namiotowego). System potrafi rozpoznać język klienta i wysłać odpowiedź w jego ojczystym języku.

## Główne funkcjonalności
- **Wielojęzyczność:** Automatyczna detekcja języka (PL, EN, DE, CS) za pomocą biblioteki `langdetect`.
- **System Anty-Spam:** Mechanizm zapobiegający wielokrotnemu wysyłaniu tych samych odpowiedzi do jednego nadawcy w ciągu doby.
- **Kategoryzacja treści:** Rozpoznawanie tematów zapytań (np. pole namiotowe vs. inne zapytania) na podstawie międzynarodowej listy słów kluczowych.
- **Zarządzanie treścią (JSON):** Szablony odpowiedzi przechowywane w osobnym pliku `replies.json`, co pozwala na zmianę treści bez ingerencji w kod.
- **Bezpieczeństwo:** Poświadczenia serwera pocztowego ukryte w zmiennych środowiskowych (`.env`).

## Struktura plików
```text
├── main.py              # Główny skrypt programu
├── replies.json         # Plik z tłumaczeniami (PL, EN, DE, CS)
├── .env                 # Plik konfiguracyjny (email, hasło) - NIE publikować na GitHub!
├── replied_emails.txt   # Baza danych obsłużonych kontaktów (generowana automatycznie)
└── README.md            # Dokumentacja projektu