from apps.products.models.products import Product
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet, Q


class ProductSelector:
    """
        Reusable product queries
    """
    @staticmethod
    def get_product_by_id(product_id) -> Product:

        return get_object_or_404(
            Product.objects.select_related('category','cpu').prefetch_related('images'),
            is_active=True, id=product_id
        )
    

    @staticmethod   
    def get_active_products()-> QuerySet:

        return Product.objects.filter(
                is_active=True
                ).select_related('category','cpu').order_by('-created_at')
            
        

    @staticmethod
    def get_product_by_slug(product_slug) -> Product:

        return get_object_or_404(
            Product.objects.select_related('category', 'cpu').prefetch_related('images'),
            is_active=True,
            slug=product_slug
        )
    

    @staticmethod
    def get_products_by_brand(product_brand) -> QuerySet:

        return Product.objects.filter(
                brand = product_brand,
                is_active = True
            ).select_related('category', 'cpu').order_by('-created_at')
    
            
    

    @staticmethod 
    def get_products_by_category(category_slug) -> QuerySet:

        return Product.objects.filter(
                category__slug = category_slug,
                is_active = True,  
            ).select_related('category', 'cpu')
        