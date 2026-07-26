from django.urls import path
from apps.assistant.api.views import assistant_view



app_name = 'chat'

urlpatterns = [

    path('', assistant_view.ChatView.as_view(), name='ai_chat')

]