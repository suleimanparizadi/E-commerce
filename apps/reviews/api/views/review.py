from rest_framework import views, status, permissions
from rest_framework.response import Response
from apps.reviews.api.serializers import review_serializer
from apps.reviews.selectors.review import ReviewSelector
from apps.accounts.permissions import IsAuthenticatedAndVerified
from apps.reviews.permissions import IsOwnerOrAdmin, HasPurchasedProduct
from apps.reviews.service.review_service import ReviewService
from apps.reviews.models.review_model import Review
from django.shortcuts import get_object_or_404

class ListProductReviewsView(views.APIView):


    """
        List all reviews for a specific product.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, product_slug:str):

        reviews = ReviewSelector.get_reviews_for_product(product_slug)
        if not reviews:

            return Response({'error':'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = review_serializer.ReviewListSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UserReviewOnProductView(views.APIView):


    """
        Get the authenticated user's review for a specific product.
    
        Requires authentication. Users can only see their own review.
    """

    permission_classes = [IsAuthenticatedAndVerified, IsOwnerOrAdmin]

    def get(self, request, product_slug:str):

        user = request.user

        review = ReviewSelector.get_user_review_for_product(user, product_slug)
        if not review:
            return Response({'error':'Review not found'}, status=status.HTTP_404_NOT_FOUND)       

        serializer = review_serializer.ReviewListSerializer(review)

        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateReviewView(views.APIView):


    """
     Create a review for a purchased product.
    
    Requires authentication and proof of purchase.
    Users can only review products they have purchased.

    """

    permission_classes = [IsAuthenticatedAndVerified, HasPurchasedProduct]

    def post(self, request, product_slug:str):

        serializer = review_serializer.ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = ReviewService(request.user)
        result, message = service.create_review(product_slug=product_slug, **serializer.validated_data)

        if not result:
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = review_serializer.ReviewListSerializer(result)
        return Response({'message':message, 'data':serializer_data.data}, status=status.HTTP_201_CREATED)



class ReviewDetailView(views.APIView):

    """
    Update or delete an existing review.
    
    Requires authentication. Users can only modify their own reviews.
    Admins can modify any review

    """

    permission_classes = [IsAuthenticatedAndVerified, IsOwnerOrAdmin]
    

    def patch(self, request, review_id:int):

        review = ReviewSelector.get_review_by_id(review_id)
        if not review:
            return Response({'error':'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = review_serializer.ReviewSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = ReviewService(request.user)
        result, message = service.update_review(review_id=review_id, **serializer.validated_data)

        if not result:

            return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)

        self.check_object_permissions(request, review)
        serializer_data = review_serializer.ReviewListSerializer(result)
        return Response({'message':message, 'review':serializer_data.data},
                    status=status.HTTP_200_OK)
    
    



    def delete(self, request, review_id:int):

        service = ReviewService(request.user)
        review = get_object_or_404(Review, id=review_id)
        success, message = service.delete_review(review_id)
        
        self.check_object_permissions(request, review)
        return Response({'message':message},
                     status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST)




        



    

