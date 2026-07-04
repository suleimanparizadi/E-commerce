from apps.products.models.products import Product
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet


class ProductSelector:
    """
        Reusable product queries
    """
    @staticmethod
    def get_product_by_id(product_id: int) -> Product:

        return get_object_or_404(
            Product.objects.select_related('category','cpu').prefetch_related('images'),
            is_active=True, id=product_id
        )
    

    @staticmethod   
    def get_active_products()-> QuerySet:

        return Product.objects.filter(
                is_active=True
                ).select_related('category','cpu').prefetch_related('images').order_by('-created_at')
            
        

    @staticmethod
    def get_product_by_slug(product_slug: str) -> Product:

        return get_object_or_404(
            Product.objects.select_related('category', 'cpu').prefetch_related('images'),
            is_active=True,
            slug=product_slug
        )
    
            
    
    @staticmethod
    def filter_product(
            brand=None, category_slug=None, ram=None, storage=None, gpu=None, 
            cpu_manufacturer=None, min_price=None, max_price=None,
            in_stock_only=None, touch_screen = None,
            min_display_size=None, max_display_size=None) -> QuerySet:
        

        product = Product.objects.filter(is_active=True)

        if brand:
            product = product.filter(brand__iexact=brand)


        if category_slug:
            product = product.filter(category__slug=category_slug)

        if ram:
            product = product.filter(ram=ram)

        if storage:
            product = product.filter(storage=storage)

        if gpu:
            product = product.filter(gpu=gpu)

        if cpu_manufacturer:
            product = product.filter(cpu__manufacturer=cpu_manufacturer)

        
        if min_price is not None:
            product = product.filter(price__gte=min_price)

        if max_price is not None: # <--- then python treat 0 as a real value too, not a False
            product = product.filter(price__lte=max_price)

        if in_stock_only:
            product = product.filter(stock__gt=0)

        
        if min_display_size:
            product = product.filter(display_size__gte=min_display_size)

        if max_display_size:
            product = product.filter(display_size__lte=max_display_size)

        if touch_screen is not None:
            product = product.filter(touch_screen=touch_screen)

        return product.select_related('cpu', 'category').prefetch_related('images')
    





