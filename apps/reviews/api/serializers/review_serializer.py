from rest_framework import serializers
from apps.reviews.models.review_model import Review
from django.contrib.auth import get_user_model

User = get_user_model()



class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review

        fields = ['rating', 'comment']

        read_only_fields =['product']



class ReviewUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User

        fields = ['first_name', 'last_name']



class ReviewListSerializer(serializers.ModelSerializer):

    user = ReviewUserSerializer(read_only=True)

    class Meta:

        model = Review

        fields = ['user', 'comment', 'rating' , 'created_at']
        
        read_only_fields = fields # Django needs fields no matter what 