from rest_framework import views, status
from rest_framework.response import Response
from apps.assistant.selectors.assistant_selectors import AssistantSelector
from apps.assistant.service.assistant_service import chat
from apps.assistant.api.serializer import assistant_serializer
from apps.accounts.permissions import IsAdmin
from apps.assistant.models.faq import FAQ
from django.shortcuts import get_object_or_404




class ChatView(views.APIView):
    
    def post(self,request):
        serializer = assistant_serializer.ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        question = serializer.validated_data['question']
        faq = AssistantSelector.get_active_faqs()

        answer = chat(question, faq)

        # Check if the response is a dict (search result with products)
        # if isinstance(answer, dict):
         #   return Response(answer, status=status.HTTP_200_OK)

        return Response({'answer':answer}, status=status.HTTP_200_OK)



class FAQListView(views.APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        faqs = FAQ.objects.all().order_by('-id')
        serializer = assistant_serializer.FAQSerializer(faqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateFAQView(views.APIView):

    permission_classes = [IsAdmin]


    def post(self, request):

        serializer = assistant_serializer.FAQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)





class UpdateFAQView(views.APIView):

    permission_classes = [IsAdmin]

    def put(self, request, faq_id):

        faq = get_object_or_404(FAQ, id=faq_id)

        serializer = assistant_serializer.FAQSerializer(faq, data=request.data ,partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class DeleteFAQView(views.APIView):

    permission_classes = [IsAdmin]


    def delete(self, request, faq_id):
        
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()

        return Response(status=status.HTTP_200_OK)
