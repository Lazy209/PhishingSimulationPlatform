import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "metrics.db"

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-only-change-in-production")
HOST = os.getenv("FLASK_HOST", "127.0.0.1")
PORT = int(os.getenv("FLASK_PORT", "5000"))
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000").rstrip("/")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USERNAME)

CAMPAIGN_NAME = os.getenv("CAMPAIGN_NAME", "Security Awareness Simulation")
