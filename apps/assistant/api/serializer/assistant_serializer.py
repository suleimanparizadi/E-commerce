from rest_framework import serializers
from apps.assistant.models.faq import FAQ


class ChatSerializer(serializers.Serializer):

    question = serializers.CharField(max_length= 500)


    


class FAQSerializer(serializers.ModelSerializer):

    class Meta:
        model = FAQ

        fields = '__all__'
