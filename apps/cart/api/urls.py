from django.urls import path
from apps.cart.api.views import cart_view

app_name = 'cart'

urlpatterns = [
    path('cart/', cart_view.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add_item/', cart_view.AddItemView.as_view(), name='add_item'),
    path('cart/clear',cart_view.ClearCartView.as_view(), name='clear_cart'),
    path('cart/item/<int:item_id>', cart_view.CartItemView.as_view(), name='cart_item'),
]