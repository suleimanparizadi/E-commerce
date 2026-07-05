from django.urls import path
from apps.products.api.views import product

app_name = 'product'

urlpatterns = [

    path('', product.ListProductView.as_view(), name='list_all_product'),
    path('search/', product.ProductSearchOrFilterView.as_view(), name='serach_product'),
    path('<slug:slug>/', product.ProductDetailView.as_view(), name='detail_product'),



]