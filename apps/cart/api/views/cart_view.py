from rest_framework import views, status
from rest_framework.response import Response
from apps.cart.selectors.cart_selectors import CartSelector
from apps.cart.services.cart_service import CartService
from apps.cart.api.serializers import cart_serializer







class CartDetailView(views.APIView):

    def get(self, request):

        if request.user.is_authenticated:
            cart = CartSelector.get_cart_by_user(request.user)

        else:
            session_key = request.session.session_key

            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            cart = CartSelector.get_cart_by_session(session_key=session_key)

        if not cart:
            return Response({'items':[]}, status=status.HTTP_200_OK)
        
        serializer = cart_serializer.CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)




class AddItemView(views.APIView):

    def post(self, request):

        serializer = cart_serializer.AddItemToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CartService(request)

        result, message = service.add_item(**serializer.validated_data)

        if not result:
            return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':message}, status=status.HTTP_200_OK)


class CartItemView(views.APIView):



    def patch(self, request, item_id):

        serializer = cart_serializer.UpdateItemSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        service = CartService(request)
        result, message = service.update_item(item_id=item_id, **serializer.validated_data)

        if not result:
            return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':message}, status=status.HTTP_200_OK)




    def delete(self, request, item_id):

        service = CartService(request)

        result, message = service.remove_item(item_id)

        if not result:
            return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':message}, status=status.HTTP_200_OK)


class ClearCartView(views.APIView):


    def delete(self, request):

        service = CartService(request)

        result, message = service.clear_cart()

        if not result:
            return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message':message}, status=status.HTTP_200_OK)

