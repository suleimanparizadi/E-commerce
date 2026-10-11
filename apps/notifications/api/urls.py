from django.urls import path
from apps.notifications.api import views

app_name = 'notifications'

urlpatterns = [
    path('telegram/generate-link/', views.GenerateLinkCodeView.as_view(), name='telegram_generate_link'),
    path('telegram/disconnect/', views.DisconnectTelegramView.as_view(), name='telegram_disconnect'),
]