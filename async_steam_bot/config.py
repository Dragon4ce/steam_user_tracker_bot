import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_MAIN_BOT_TOKEN = os.getenv("BOT_API_TOKEN")
TELEGRAM_NOTIFIER_BOT_TOKEN = os.getenv("NOTIFIER_BOT_TOKEN")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
db_path = os.getenv("DATABASE_PATH")