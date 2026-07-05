from rest_framework.response import Response
from apps.products.api.serializer import product_serializer
from rest_framework import views, status
from apps.products.selectors.product import ProductSelector 



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


            # if user didn't put the touch screen in the filter means dosn't matter
            # it will return None as false
            # touch screen fileds must return True or False or None
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
        



