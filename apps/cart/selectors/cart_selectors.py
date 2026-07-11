from apps.cart.models.cart import Cart




class CartSelector:

    def get_cart_with_items(self, cart):

        return Cart.objects.filter(id=cart.id).first()

