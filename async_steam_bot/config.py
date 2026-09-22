import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_API_TOKEN")
NOTIFIER_BOT_TOKEN = os.getenv("NOTIFIER_BOT_TOKEN")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
