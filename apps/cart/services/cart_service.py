from apps.cart.models.cart import Cart, CartItem 
from apps.products.models.products import Product
from django.db import transaction




class CartService:

    def __init__(self, request):
        self.request = request


    def _get_or_create_cart(self):

        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)

        else:
            session_key = self.request.session.session_key
            if not session_key:
                self.request.session.create()
                session_key = self.request.session.session_key

            cart , _ = Cart.objects.get_or_create(session_key=session_key)
        
        return cart
    

    @staticmethod
    def _check_stock(product, requested_quantity):

        if product.stock < requested_quantity:
            return False, f"only {product.stock} items left in the stock"

        return True, None


    def add_item(self, product_slug, quantity=1):       

        cart = self._get_or_create_cart()

        try:
            product = Product.objects.get(is_active=True, slug=product_slug)
        
        except Product.DoesNotExist:
            return False, "Cannot find the product"
        
        existing = CartItem.objects.filter(cart=cart,product=product).first()

        if existing:

            total_quantity = existing.quantity + quantity
            success, message = CartService._check_stock(product, total_quantity)

            if not success:
                return False, message
            
            if total_quantity > CartItem.MAX_ORDER_QUANTITY:
                return False, f"Maximum {CartItem.MAX_ORDER_QUANTITY} units per product allowed."
            
            
            existing.quantity += quantity
            existing.save(update_fields=['quantity'])
            return existing, "Quantity updated."
        
        else:
           
            success, message = CartService._check_stock(product, quantity)

            if not success:
                return False, message
            

            item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

            return item, "Item added to cart."
    


    def update_item(self, quantity, item_id):

        if quantity < 1:
            return False, "Quantity must be at least 1." 
        
        if quantity > CartItem.MAX_ORDER_QUANTITY:
            return False, f"Maximum {CartItem.MAX_ORDER_QUANTITY} units per product allowed."

        cart = self._get_or_create_cart()

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)

        except CartItem.DoesNotExist:
            return False, "Item not found in your cart."
        
        
        success, message = CartService._check_stock(item.product, quantity)
        if not success:
            return False, message


        item.quantity = quantity
        item.save(update_fields=['quantity'])

        return item, "Quantity updated"
        

    

    def remove_item(self, item_id):

        
        cart = self._get_or_create_cart()

        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
         
        except CartItem.DoesNotExist:
            return False, "Item not found in your cart."
        
        item.delete()

        return True, "Item removed from cart successfully."
    


    def clear_cart(self):
        
        cart = self._get_or_create_cart()
        cart.delete()
       
        return True ,"Cart successfully removed"





    @transaction.atomic
    @staticmethod
    def merge_carts(session_key, user):

        if not session_key:
            return False, "No guest cart to merge."
        
        try:
            guest_cart = Cart.objects.select_for_update().get(session_key=session_key)
        except Cart.DoesNotExist:
            return False, "No guest cart found."
        
        user_cart, _ = Cart.objects.select_for_update().get_or_create(user=user)
        
        for item in guest_cart.items.all():
            existing = user_cart.items.filter(product=item.product).first()
           
            if existing:
                    
                requested_quantity = existing.quantity + item.quantity

                success, message = CartService._check_stock(item.product, requested_quantity)

                if not success:
                    return False, message

                new_quantity = min(requested_quantity, CartItem.MAX_ORDER_QUANTITY)
                existing.quantity = new_quantity
                existing.save(update_fields=['quantity'])
            else:
                item.cart = user_cart
                item.save(update_fields=['cart'])
        
        guest_cart.delete()
        return user_cart, "Carts merged successfully."

                

