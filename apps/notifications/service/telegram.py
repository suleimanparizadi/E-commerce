import os
import requests


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')


class TelegramNotifier:
    """Send messages to admin via Telegram."""

    @staticmethod
    def send(message: str) -> bool:
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_CHAT_ID:
            return False

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        try:
            response = requests.post(url, json={
                'chat_id': TELEGRAM_ADMIN_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML',
            }, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False