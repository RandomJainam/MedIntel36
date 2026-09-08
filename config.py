from pathlib import Path
import os
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Project Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
FEATURE_STORE_DIR = DATA_DIR / "feature_store"
GOLD_DIR = DATA_DIR / "gold"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "medintel360.db"

REPORT_DIR = BASE_DIR / "reports"

# -----------------------------
# Database
# -----------------------------
DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

# -----------------------------
# OpenRouter
# -----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL_NAME = "deepseek/deepseek-chat-v3-0324"

# -----------------------------
# App
# -----------------------------
APP_NAME = "MedIntel360"

VERSION = "1.0.0"