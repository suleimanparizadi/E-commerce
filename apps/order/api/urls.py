from django.urls import path
from apps.order.api.views import order_view

app_name = 'order'


urlpatterns = [

    path('checkout/', order_view.CheckoutView.as_view(), name='checkout'),
    path('', order_view.ListUsersOrders.as_view(), name='list_orders'),
    path('order_detail/<int:order_id>/', order_view.OrderDetailView.as_view(),
                                                name='detail_order'),


]