from rest_framework import serializers
from apps.products.models.products import Product, CPU
from apps.products.models.image import ProductImage
from apps.products.models.category import Category


class CPUSerializer(serializers.ModelSerializer):

    class Meta:
        model = CPU
        
        fields = '__all__'



class CPUSummarySerializer(serializers.ModelSerializer):
    class Meta:

        model = CPU
        fields = ['manufacturer', 'series', 'model']



class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage 

        fields = ['images', 'alt_text']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = ['name', 'slug', 'parent']



class ProductListSerializer(serializers.ModelSerializer):

    cpu = CPUSummarySerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'brand', 'price', 'thumbnail', 
                  'ram', 'storage', 'gpu', 'cpu', 'is_in_stock', 'category']
        

class ProductDetailSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    cpu = CPUSerializer(read_only=True)
    category = CategorySerializer(read_only=True)


    class Meta:

        model = Product

        fields = ['name', 'slug', 'brand', 'price', 'thumbnail', 
                  'ram', 'storage', 'gpu', 'is_in_stock',
                  'description', 'cpu', 'on_board_gpu',
                  'touch_screen', 'display_size', 'category', 'image']