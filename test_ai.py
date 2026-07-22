import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.assistant.service.assistant_service import ask_ai
from apps.assistant.models.faq import FAQ

faqs = FAQ.objects.filter(is_active=True)
question = "مرجوعی هم دارید؟"
print(f"User: {question}")
answer = ask_ai(question, faqs)
print(f"AI: {answer}")