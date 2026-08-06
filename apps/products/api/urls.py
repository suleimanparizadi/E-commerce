from django.urls import path
from apps.products.api.views import product

app_name = 'products'

urlpatterns = [

    path('', product.ListProductView.as_view(), name='list_all_product'),
    path('search/', product.ProductSearchOrFilterView.as_view(), name='search_product'),
    path('create/', product.ProductCreateView.as_view(), name='create_product'),
    path('cpu/', product.GetCPUView.as_view(), name='get_cpu'),
    path('category', product.GetCategoryView.as_view(), name='get_category'),
    path('admin/<slug:slug>/delete/', product.ProductDeleteView.as_view(), name='delete_product'),
    path('admin/<slug:slug>/update/', product.ProductUpdateView.as_view(), name='update_product'),
    path('<slug:slug>/', product.ProductDetailView.as_view(), name='detail_product'),
    

]