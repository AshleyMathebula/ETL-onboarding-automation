import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
MAILBOX=os.getenv("MAILBOX", "INBOX")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", 120))

def validate_config():
    missing = [] # List to track missing configurations
    
    if not EMAIL_HOST:
        missing.append("EMAIL_HOST")
    if not EMAIL_USER:
        missing.append("EMAIL_USER")
    if not EMAIL_PASSWORD:
        missing.append("EMAIL_PASSWORD")
    
    if missing:
        raise ValueError(f"Missing required email configuration: {', '.join(missing)}")