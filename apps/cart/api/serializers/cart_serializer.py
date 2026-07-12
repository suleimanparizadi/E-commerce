from rest_framework import serializers
from apps.cart.models.cart import Cart, CartItem
from apps.products.models.products import Product


class CartProductSerializer(serializers.ModelSerializer):
    """
    Lightweight product info shown inside each cart item.
    Used inside CartItemSerializer — not directly by CartSerializer.
    """

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'thumbnail', 'in_stock']


class CartItemSerializer(serializers.ModelSerializer):
    """
    A single line item in the cart.
    Includes quantity + nested product details.
    Used by CartSerializer to show all items in the cart.
    """

    product = CartProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    The full cart for display.
    Contains all items (with nested products), created_at, and updated_at.
    Used for the GET /api/cart/ response.
    """

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['items', 'created_at', 'updated_at']


class AddItemToCartSerializer(serializers.Serializer):
    """
    Validates input for POST /api/cart/add/.
    Accepts product_slug and optional quantity (defaults to 1 in the service).
    """

    product_slug = serializers.SlugField()
    quantity = serializers.IntegerField(
        min_value=1, max_value=CartItem.MAX_ORDER_QUANTITY
    )


class UpdateItemSerializer(serializers.Serializer):
    """
    Validates input for PATCH /api/cart/items/{id}/.
    Accepts a new quantity value.
    """

    quantity = serializers.IntegerField(
        min_value=1, max_value=CartItem.MAX_ORDER_QUANTITY
    )


    