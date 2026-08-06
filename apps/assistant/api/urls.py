from django.urls import path
from apps.assistant.api.views import assistant_view



app_name = 'chat'

urlpatterns = [

    path('', assistant_view.ChatView.as_view(), name='ai_chat'),
    path('admin/create_faq/', assistant_view.CreateFAQView.as_view(), name='create_faq'),
    path('admin/update_faq/<int:faq_id>/', assistant_view.UpdateFAQView.as_view(), name='update_faq'),
    path('admin/delete_faq/<int:faq_id>/', assistant_view.DeleteFAQView.as_view(), name='delete_view'),

]