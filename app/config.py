from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
URL = os.getenv("URL")
CLIENT_URL = os.getenv("CLIENT_URL")
JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SMTP_HOST = os.getenv("MAIL_SMTP_HOST")
MAIL_SMTP_PORT = os.getenv("MAIL_SMTP_PORT")
MAIL_EMAIL = os.getenv("MAIL_EMAIL")
