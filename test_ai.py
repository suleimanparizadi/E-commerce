
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.assistant.service.assistant_service import chat
from apps.assistant.models.faq import FAQ

faqs = FAQ.objects.filter(is_active=True)
question = "سازنده ی این پروژه کیه؟"
print(f"User: {question}")
answer = chat(question, faqs)
print(f"AI: {answer}")


