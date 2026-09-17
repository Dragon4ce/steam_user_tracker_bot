import os
db_path = os.getenv('DB_PATH', 'data/async_steam_checker_bot_database.db')
TELEGRAM_MAIN_BOT_TOKEN = '8838382646:AAG240WOi2HoKGPl-rs4I2JNq6ekMkh3Gdo'
TELEGRAM_NOTIFIER_BOT_TOKEN = '8913035791:AAEJeqgiNzk4EtcbV_TMPfwchXMCAz2_oe8'
STEAM_API_KEY = "4CDC3A96B5819263C68FE3B4C4A352A7"
online_status = {
    '0': '🔴**Оффлайн**🔴 ***(Возможно скрытый профиль!)***',
    '1': '🟢**Онлайн**🟢',
    '2': '⛔**Занят**⛔',
    '3': '⌛**Не на месте**⌛',
    '4': '💤**Спит**💤'
}
BATTLEMETRICS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjY1YTdlZjMxZDYyNDBlNTQiLCJpYXQiOjE3Njc1NDYyMDYsIm5iZiI6MTc2NzU0NjIwNiwiaXNzIjoiaHR0cHM6Ly93d3cuYmF0dGxlbWV0cmljcy5jb20iLCJzdWIiOiJ1cm46dXNlcjo1NTE0ODAifQ.aCFF_yphu8IQ3PrcbyWfqEepOaKc0x6XxuT7cc62XM8"
BASE_URL = "https://api.battlemetrics.com"
HEADERS = {
    "Authorization": f"My first tgbot token {BATTLEMETRICS_API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "MyBattlemetricsApp/1.0"
}