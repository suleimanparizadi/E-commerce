from apps.order.models.order_model import Order, OrderItem


class CheckoutService:
    
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart
    


    def _calculate_total(self):
        ...
    
    def _create_order_items(self, order):
        ...
    
    def _deduct_stock(self):
        ...
    
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
    