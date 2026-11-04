import secrets
from django.core.cache import cache


LINK_CODE_PREFIX = 'telegram_link:'
LINK_CODE_TIMEOUT = 600  # 10 minutes


class TelegramLinkService:

    @staticmethod
    def generate_link_code(user):
        """Generate a code for the user to send to the bot."""
        code = secrets.token_hex(3).upper()  # 6-char code like "A3F9C2"
        cache.set(f"{LINK_CODE_PREFIX}{code}", user.id, timeout=LINK_CODE_TIMEOUT)
        return code

    @staticmethod
    def consume_link_code(code):
        """Called by the bot when a user sends the code. Returns user_id or None."""
        user_id = cache.get(f"{LINK_CODE_PREFIX}{code}")
        if user_id:
            cache.delete(f"{LINK_CODE_PREFIX}{code}")
        return user_id

    @staticmethod
    def link_user(user, chat_id):
        """Save the chat_id to the user record."""
        user.telegram_chat_id = chat_id
        user.save(update_fields=['telegram_chat_id'])
        return True

    @staticmethod
    def unlink_user(user):
        """Remove the chat_id from the user record."""
        user.telegram_chat_id = None
        user.save(update_fields=['telegram_chat_id'])
        return True