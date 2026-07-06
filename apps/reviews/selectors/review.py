from apps.reviews.models.review_model import Review
from django.db.models import QuerySet
from apps.products.models.products import Product
from django.contrib.auth import get_user_model


User = get_user_model()



class ReviewSelector:

    @staticmethod
    def get_reviews_for_product(product_slug : str) -> QuerySet | None:
        

        try:
            product = Product.objects.get(slug=product_slug)

        except Product.DoesNotExist:
            return None

        return product.reviews.select_related('user').all()
    



    @staticmethod
    def get_user_review_for_product(user, product_slug) -> Review | None:
        
        try:
        
            product = Product.objects.get(slug=product_slug)
        
        except Product.DoesNotExist:
            return None

        return product.reviews.filter(user=user).first()
    

    @staticmethod
    def get_review_by_id(review_id : int) -> Review :

        return Review.objects.get(id=review_id)


    @staticmethod
    def get_all_user_reviews(user_id:int) -> QuerySet | None :
        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return None
        
        return Review.objects.filter(user=user).select_related('product').all()
