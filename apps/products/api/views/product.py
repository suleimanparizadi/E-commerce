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

        return Response(serializer.data)
    



class ProductDetailView(views.APIView):

    def get(self, request, slug):

        product = ProductSelector.get_product_by_slug(slug)

        serializer = product_serializer.ProductDetailSerializer(product)

        return Response(serializer.data)




class ProductSearchView(views.APIView):


    def get(self, request):

        product = ProductSelector.filter_product
