from rest_framework import serializers
from apps.reviews.models.review_model import Review
from django.contrib.auth import get_user_model

User = get_user_model()



class ReviewSerializer(serializers.ModelSerializer):


    """
    Used for CREATE and UPDATE operations.
    Accepts rating and comment from the user.
    Product is set by the view (read-only to the user).

    """


    class Meta:
        model = Review

        fields = ['rating', 'comment', 'product']

        read_only_fields =['product']



class ReviewUserSerializer(serializers.ModelSerializer):

    """
        Nested serializer for displaying review author info.
        Shows only first_name and last_name — no phone number or email.
        Used inside ReviewListSerializer.
    """



    class Meta:
        model = User

        fields = ['first_name', 'last_name']





class ReviewListSerializer(serializers.ModelSerializer):


    """
    Used for GET (read-only) operations.
    Displays a review with nested user info, rating, comment, and created_at.
    All fields are read-only — not used for creating or updating.
    
    """


    user = ReviewUserSerializer(read_only=True)

    class Meta:

        model = Review

        fields = ['user', 'comment', 'rating' , 'created_at']
        
        read_only_fields = fields # Django needs fields no matter what 