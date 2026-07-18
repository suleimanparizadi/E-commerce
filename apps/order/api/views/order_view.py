from rest_framework import views, status
from rest_framework.response import Response
from apps.order.service.order_service import CheckoutService
from apps.accounts.permissions import IsAuthenticatedAndVerified
from apps.order.api.serializer import order_serializer
from apps.order.models.order_model import Order
from apps.cart.selectors.cart_selectors import CartSelector
from django.shortcuts import get_object_or_404




class CheckoutView(views.APIView):
    permission_classes = [IsAuthenticatedAndVerified]


    def post(self, request):

        serializer = order_serializer.CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        user_cart = CartSelector.get_cart_by_user(user=request.user)
        
        if not user_cart:
            return Response({'message':"Unable to find the cart"},
                            status=status.HTTP_400_BAD_REQUEST)
        

        service = CheckoutService(cart=user_cart, user=request.user)
        order, message = service.checkout(**serializer.validated_data)

        if not order:
            return Response({'message':message},status=status.HTTP_400_BAD_REQUEST)
        
        serialized_order = order_serializer.OrderSerializer(order)
        return Response({'data':serialized_order.data, 'message':message}
                        , status=status.HTTP_201_CREATED)
    



class ListUsersOrders(views.APIView):

    permission_classes = [IsAuthenticatedAndVerified]


    def get(self, request):
        

        
        user_orders = Order.objects.filter(user=request.user)

        if not user_orders.exists():
            return Response([], status=status.HTTP_200_OK)


        serializer = order_serializer.OrderSerializer(user_orders, many=True)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)




class OrderDetailView(views.APIView):

    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request, order_id):

       
        user_order = get_object_or_404(Order ,user=request.user, id=order_id)
      

        serializer = order_serializer.OrderSerializer(user_order)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
    





