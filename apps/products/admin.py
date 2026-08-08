from django.contrib import admin
from apps.products.models.products import Product, CPU
from apps.products.models.category import Category
from apps.products.models.image import ProductImage
from apps.reviews.models.review_model import Review



class ReviewInline(admin.TabularInline):
    model = Review
    fields = ['user', 'rating', 'comment', 'created_at']
    readonly_fields = ['created_at']
    extra = 0
    can_delete = True


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'brand', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'brand', 'is_active', 'on_board_gpu', 'touch_screen', 'cpu__manufacturer']
    search_fields = ['name', 'brand', 'description']
    prepopulated_fields = {'slug': ('name', 'brand')}
    inlines = [ProductImageInline, ReviewInline]      
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'brand', 'slug', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('Specifications', {
            'fields': ('cpu', 'ram', 'storage', 'gpu', 'on_board_gpu', 'display_size', 'touch_screen')
        }),
        ('Media', {
            'fields': ('thumbnail',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }), 
    )


@admin.register(CPU)
class CPUAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'series', 'model', 'cores']
    list_filter = ['manufacturer']
    search_fields = ['series', 'model']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'alt_text', 'created_at']
    search_fields = ['product__name', 'alt_text']