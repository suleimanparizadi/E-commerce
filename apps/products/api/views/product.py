from rest_framework.response import Response
from apps.products.api.serializer import product_serializer
from rest_framework import views, status
from apps.products.selectors.product import ProductSelector 
from apps.accounts.permissions import IsAdmin
from apps.products.models.products import CPU
from apps.products.models.category import Category

class ListProductView(views.APIView):

    """
        List all active products.
    """

    def get(self, request):


        product = ProductSelector.get_active_products()

        serializer = product_serializer.ProductListSerializer(product, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    



class ProductDetailView(views.APIView):

    def get(self, request, slug):

        product = ProductSelector.get_product_by_slug(slug)

        serializer = product_serializer.ProductDetailSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)




class ProductSearchOrFilterView(views.APIView):


    def get(self, request):

        search_query = request.query_params.get('q', '').strip()

        if search_query:
            product = ProductSelector.search_product(search_query)

        else:
            brand=request.query_params.get("brand")
            category_slug=request.query_params.get("category_slug")
            ram=request.query_params.get("ram")
            storage=request.query_params.get("storage")
            min_price=request.query_params.get("min_price")
            max_price=request.query_params.get("max_price")
            gpu=request.query_params.get("gpu")
            cpu_manufacturer=request.query_params.get("cpu_manufacturer")


            min_display_size=request.query_params.get("min_display_size")
            max_display_size=request.query_params.get("max_display_size")

            # if query_params is not empty it'll always return True
            # make sure its only return true when it is true
            in_stock_only=request.query_params.get("in_stock_only", '').lower() == 'true'


            # if user didn't put the touch screen in the filter means doesn't matter
            # it will return None as false
            # touch screen fields must return True or False or None
            touch_screen_param = request.query_params.get('touch_screen')
            if touch_screen_param is not None:
                touch_screen = touch_screen_param.lower() == 'true'
            else:
                touch_screen = None




            product = ProductSelector.filter_product(
                brand=brand, category_slug=category_slug, ram=ram, storage=storage,
                min_price=min_price, max_price=max_price, gpu=gpu,
                cpu_manufacturer=cpu_manufacturer, min_display_size=min_display_size,
                max_display_size=max_display_size, in_stock_only=in_stock_only,
                touch_screen=touch_screen
            )


        serializer = product_serializer.ProductListSerializer(product, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        


#_____________Admin________________________________

class ProductCreateView(views.APIView):

    permission_classes = [IsAdmin]
    
    def post(self, request):
        serializer = product_serializer.AdminProductWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)




class ProductUpdateView(views.APIView):


    permission_classes = [IsAdmin]
    
    def put(self, request, slug):
        product = ProductSelector.get_product_by_slug(slug)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = product_serializer.AdminProductWriteSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductDeleteView(views.APIView):


    permission_classes = [IsAdmin]
    
    def delete(self, request, slug):
        product = ProductSelector.get_product_by_slug(slug)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_200_OK)




class GetCPUView(views.APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        cpu = CPU.objects.all()

        serializer = product_serializer.CPUSummarySerializer(cpu, many=True)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)





class GetCategoryView(views.APIView):

    permission_classes = [IsAdmin]

    def get(self, request):

        category = Category.objects.all()

        serializer = product_serializer.CategorySerializer(category, many=True)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)