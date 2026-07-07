from django.urls import path
from apps.reviews.api.views import review

app_name = 'reviews'

urlpatterns = [

    path('product/<slug:product_slug>/list', review.ListProductReviewsView.as_view(),
                                    name='list_product_reviews'),

    path('product/<slug:product_slug>/create/', review.CreateReviewView.as_view(),
                                    name='create_product_view'),

     path('<int:review_id>/change/', review.ReviewDetailView.as_view(),
                                    name='edit/remove_review'),

]
