from django.contrib.auth import get_user_model
from apps.products.models.products import Product
from apps.reviews.models.review_model import Review



User = get_user_model()



class ReviewService:

    def __init__(self, user):
        self.user = user


    def create_review(self, product_slug, comment, rating):
        

        try:
            product = Product.objects.get(slug=product_slug)

        except Product.DoesNotExist:
            return False, "Unable to find the product"

        review = Review.objects.filter(
            user=self.user, product=product).exists()

        if review:
            return False, "you already reviewed this product"
        

        review = Review.objects.create(
            user=self.user, product=product, rating=rating,
            comment=comment
        )
        
        return review, "Review created successfully."





    def delete_review(self, review_id):

        try:
            review = Review.objects.get(id=review_id)

        except Review.DoesNotExist:
            return False, "Unable to find this review"
    
        
        review.delete()
        return True, "review deleted successfully."




    def update_review(self, review_id, comment, rating):

        try:

            review = Review.objects.get(id=review_id)

        except Review.DoesNotExist:
            return False, "Unable to find this review"

        review.comment = comment or '' # to avoid save comment as None
        review.rating = rating
        review.save(update_fields=['comment', 'rating'])

        return review, "Review updated successfully."





