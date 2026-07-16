from apps.order.models.order_model import Order, OrderItem
from django.db import transaction 

class CheckoutService:
    
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart
        self.items = list(self.cart.items.select_related('product'))    


    def _calculate_total(self):

        total = 0 
        for item in self.items:
            total += item.quantity * item.product.price

        return total
    


    def _create_order_items(self, order):
        

    
        for item in self.items:
            OrderItem.objects.create(
                order=order, product=item.product,
                quantity=item.quantity, price_at_purchase=item.product.price
            )
    

    def _deduct_stock(self):

     for item in self.items:
         item.product.stock -= item.quantity
         item.product.save(update_fields=['stock'])
    
    
    def _notify_admin(self, order):
        print(f"New order received: Order #{order.id}")
        print(f"User: {order.user.get_full_name()}")
        print(f"Total: {order.total_amount} Rial")
        print(f"Items: {order.order_items.count()}")




    @transaction.atomic
    def checkout(self, shipping_address, shipping_city, shipping_postal_code):


        if not self.cart.items.exists():
            return False, "The cart is empty"
        

        total = self._calculate_total()

        order = Order.objects.create(user=self.user,
                                     shipping_city=shipping_city,
                                     shipping_address=shipping_address,
                                     shipping_postal_code=shipping_postal_code,
                                     total_amount=total)
        
        self._create_order_items(order)
        self._deduct_stock()        
        
        self.cart.delete()

        
        self._notify_admin(order)
        

        return order, "Order created successfully"
    