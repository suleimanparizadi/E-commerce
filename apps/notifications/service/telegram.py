import os
import requests


class TelegramNotifier:
    """Send Telegram messages to users."""

    @staticmethod
    def send_message(chat_id, message):
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token or not chat_id:
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"

        try:
            response = requests.post(url, json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML',
            }, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @staticmethod
    def send_to_user(user, message):
        """Send to a specific user if they've linked Telegram."""
        if not user.telegram_chat_id:
            return False
        return TelegramNotifier.send_message(user.telegram_chat_id, message)

    @staticmethod
    def notify_admins(message):
        """Send to all admins with linked Telegram."""
        from django.contrib.auth import get_user_model
        User = get_user_model()

        admins = User.objects.filter(
            is_staff=True,
            telegram_chat_id__isnull=False,
            is_active=True,
        )

        results = []
        for admin in admins:
            results.append(TelegramNotifier.send_to_user(admin, message))

        return results