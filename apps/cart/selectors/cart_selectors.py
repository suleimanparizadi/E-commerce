from apps.cart.models.cart import Cart


class CartSelector:
    
    @staticmethod
    def get_cart_by_session(session_key):
        return Cart.objects.prefetch_related('items__product').filter(session_key=session_key).first()

    @staticmethod
    def get_cart_by_user(user):
        return Cart.objects.prefetch_related('items__product').filter(user=user).first()