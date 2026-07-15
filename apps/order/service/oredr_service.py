from apps.order.models.order_model import Order, OrderItem
from apps.cart.models.cart import Cart, CartItem

class CheckoutService:
    
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart
    


    def _calculate_total(self):

        total = 0 
        for item in self.cart.items:
            total += item.quantity + item.product.price

        return total
    


    def _create_order_items(self, order):
        ...
    


    def _deduct_stock(self):

     for item in self.cart.items.all():
         item.product.quantity -= item.quantity
         item.product.save(update_fields=['stock'])
    
    
    
    
    def _notify_admin(self, order):
        ...


    def checkout(self, shipping_address, shipping_city):
        # 1. Validate cart is not empty
        # 2. Calculate total amount
        # 3. Create Order
        # 4. Create OrderItems from CartItems (snapshot prices)
        # 5. Deduct stock
        # 6. Clear cart
        # 7. Send admin notification (stub)
        # 8. Return order
        ...
    