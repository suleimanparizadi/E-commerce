from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from apps.products.api.views import product as product_view
from apps.products.models.products import Product, CPU
from apps.products.models.category import Category
from rest_framework import status

class TestProductView(TestCase):


    def setUp(self):



        self.client = APIClient()
        self.detail_url = reverse('product:detail_product', kwargs={'slug': 'lenovo-thinkpad'})
        self.list_url = reverse('product:list_all_product')
        self.search_url = reverse('product:search_product')

        self.category = Category.objects.create(
            name="Laptop",
            slug="laptop"
        )

        self.cpu = CPU.objects.create(
            manufacturer="INTEL",
            series="Core i7",
            model="12700H",
            cores=14
        )

        self.product1 = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="Lenovo ThinkPad",
            brand="Lenovo",
            price=35000000,
            stock=5,
            ram=16,
            storage=512,
            gpu="RTX 4060",
            slug="lenovo-thinkpad",
            on_board_gpu=False,
            touch_screen= False
        )

        self.product2 = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="Lenovo Laptop",
            brand="Lenovo",
            price=30000000,
            ram=16,
            storage=512,
            gpu="RTX 4060",
            is_active=True,
        )

        self.product3 = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="Lenovo Laptop",
            brand="Lenovo",
            price=20000000,
            ram=8,
            storage=256,
            gpu="RTX 2080",
            is_active=True,
            )
        

        self.inactive_product = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="Inactive Laptop",
            brand="Lenovo",
            price=10000000,
            ram=8,
            storage=256,
            gpu="Integrated",
            slug="inactive-laptop",
            is_active=False,
        )




    def test_list_all_product(self):
        
        """
        test all active products in list
        """

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


    def test_detail_product_view(self):

        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Lenovo ThinkPad')



    def test_detail_inactive_product_returns_404(self):

        url = reverse('product:detail_product', kwargs={'slug': 'inactive-laptop'}) 

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_filter_product(self):

        response = self.client.get(self.search_url, {'brand': 'Lenovo'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)


    def test_filter_no_result(self):
        response = self.client.get(self.search_url, {'brand':'Apple'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    def test_search_product(self):

        response = self.client.get(self.search_url, {'q':'ThinkPad'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    