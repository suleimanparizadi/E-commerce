from rest_framework import views, status
from rest_framework.response import Response
from apps.assistant.selectors.assistant_selectors import AssistantSelector
from apps.assistant.service.assistant_service import ask_ai
from apps.assistant.api.serializer import assistant_serializer


class ChatView(views.APIView):
    
    def post(self,request):
        serializer = assistant_serializer.ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        question = serializer.validated_data['question']
        faq = AssistantSelector.get_active_faqs()

        answer = ask_ai(question, faq)

        return Response({'answer':answer}, status=status.HTTP_200_OK)