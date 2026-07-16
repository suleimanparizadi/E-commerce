from rest_framework import serializers
from apps.order.models.order_model import Order, OrderItem
from apps.cart.api.serializers.cart_serializer import CartProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
    class Meta:
        model = OrderItem 
        fields = ['product', 'quantity', 'price_at_purchase']



class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'shipping_address', 
                  'shipping_city', 'shipping_postal_code', 'items', 'created_at']
        
        read_only_fields = ['total_amount']


class CheckoutSerializer(serializers.Serializer):

    
    shipping_address = serializers.CharField()
    shipping_city = serializers.CharField(max_length=125)
    shipping_postal_code = serializers.CharField()