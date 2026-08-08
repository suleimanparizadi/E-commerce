from django.contrib import admin
from apps.reviews.models.review_model import Review
from apps.products.admin import ProductAdmin







@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['product__name', 'user__phone_number', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user', 'product']