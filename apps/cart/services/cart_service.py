from apps.cart.models.cart import Cart, CartItem
from apps.products.models.products import Product

class CartService:

    def __init__(self, request):
        self.request = request
        


    def _get_or_create_cart(self):

        if self.request.user.is_authenticated:
            cart = Cart.objects.get_or_create(user=self.request.user)

        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key

            cart = Cart.objects.get_or_create(session_key=session_key)
        
        return cart
    

    def add_item(self, product_slug, quantity=1):       

        cart, _ = self._get_or_create_cart()

        try:
            product = Product.objects.get(is_active=True, slug=product_slug)
        
        except Product.DoesNotExist:
            return False, "Cannot find the product"
        
        existing = CartItem.objects.filter(cart=cart,product=product).first()
        if existing:
            if existing.quantity + quantity > 5:
                return False, "Maximum 5 units per product allowed."
            
            existing.quantity += quantity
            existing.save(update_fields=['quantity'])

        item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        return item, "Item added to cart."
    


    def update_item(self, quantity, item_id):

        if quantity < 1:
            return False, "Quantity must be at least 1." 
        
        if quantity > 5:
            return False, "Maximum 5 units per product allowed."

        cart, _ = self._get_or_create_cart()

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)

        except CartItem.DoesNotExist:
            return False, "Item not found in your cart."
        
        item.quantity = quantity
        item.save(update_fields=['quantity'])

        return item, "Quantity updated"
        

    

    def remove_item(self, item_id):

        
        cart, _ = self._get_or_create_cart()

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
         
        except CartItem.DoesNotExist:
            return False, "Item not found in your cart."
        
        item.delete()

        return True, "Item removed from cart successfully."
    


    def clear_cart(self):
        ...



    @staticmethod
    def merge_carts(session_key, user):

        if not session_key:
            return False, "No guest cart to merge."
        

        try:
            guest_cart = Cart.objects.get(session_key=session_key)
        
        except Cart.DoesNotExist:
            return False, "No guest cart found."
        

        user_cart = Cart.objects.get_or_create(user=user)

        for item in guest_cart.items.all():

            existing = user_cart.items.filter(product=item.product).first()

            if existing:
                if existing.quantity + item.quantity > 5:
                    return False, "Maximum 5 units per product allowed."
                existing.quantity += item.quantity
                existing.save(update_fields=['quantity'])
            

        
                




        
