from django.urls import path
from apps.reviews.api.views import review

app_name = 'reviews'

urlpatterns = [
    
    path('product/<slug:product_slug>/list/', review.ListProductReviewsView.as_view(),
         name='list_product_reviews'),

    
    path('product/<slug:product_slug>/create/', review.CreateReviewView.as_view(),
         name='create_review'),

    path('product/<slug:product_slug>/my-review/', review.UserReviewOnProductView.as_view(),
         name='user_review'),

    path('<int:review_id>/', review.ReviewDetailView.as_view(),
         name='review_detail'),
]