# Camping Auto-Receptionist

### An intelligent email assistant featuring language detection and anti-spam mechanisms.

## About the Project
This project was designed to optimize the workflow of a campsite reception desk. The program automates email inquiry handling, freeing staff from answering repetitive questions (e.g., regarding campsite availability). The system automatically detects the customer's language and sends a professional response in their native tongue.

## Key features
- **Multilingual Support:** Automatic language detection (PL, EN, DE, CS) using the `langdetect` library.
- **Anti-Spam System:** A mechanism that prevents sending duplicate automated responses to the same sender within a 24-hour period.
- **Content Categorization:** Recognition of inquiry topics (e.g., tent pitches vs. general inquiries) based on an international keyword list.
- **Content Management (JSON):** Response templates are stored in a separate `replies.json` file, allowing for easy content updates without modifying the source code.

## File Structure
```text
├── main.py              # Main application script
├── replies.json         # Translation file (PL, EN, DE, CS)
├── .env                 # Configuration file (email, password) - to be created manually
├── replied_emails.txt   # Log database of handled contacts (auto-generated)
└── README.md            # Project documentation
```

## Installation and Setup

1. **Install Dependencies**
   ```bash
   pip install python-dotenv python-dotenv

2. **Environment Configuration**
    Create a .env file in the root directory and fill in your credentials:         
    EMAIL_USER=twoj-email@_.com           
    EMAIL_PASS=twoje-haslo-aplikacji

4. **Run the Application**
   ```bash
   python main.py
