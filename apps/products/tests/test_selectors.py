from django.test import TestCase
from apps.products.models.products import Product, CPU
from apps.products.models.category import Category
from apps.products.selectors.product import ProductSelector


class ProductSelectorTests(TestCase):

    def setUp(self):

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

        self.product = Product.objects.create(
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


    def test_get_product_by_slug(self):

        product = ProductSelector.get_product_by_slug('lenovo-thinkpad')       
        self.assertEqual(product.id, self.product.id)



    def test_get_product_by_id(self):

        product = ProductSelector.get_product_by_id(self.product.id)
        self.assertEqual(product.id, self.product.id)

    
    def test_get_active_product(self):

        product = ProductSelector.get_active_products()
        self.assertEqual(product.count(), 1)


    def test_get_active_products_excludes_inactive(self):

        Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="Inactive Laptop",
            brand="Test",
            price=10000000,
            ram=8,
            storage=256,
            gpu="Integrated",
            slug="inactive-laptop",
            is_active=False,
        )
        
        products = ProductSelector.get_active_products()
        
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().id, self.product.id)



    def test_filter_by_brand(self):

        Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            name="test Laptop",
            brand="Lenovo",
            price=10000000,
            ram=8,
            storage=256,
            gpu="Integrated",
            slug="inactive-laptop",
            is_active=True,
        )


        product = ProductSelector.filter_product(brand='Lenovo')

        self.assertTrue(product)
        self.assertEqual(product.count(), 2)


    
    def test_filter(self):


        Product.objects.create(
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
        Product.objects.create(
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


        product = ProductSelector.filter_product(brand="Lenovo", ram=16, storage=512)

        self.assertEqual(product.count(), 2)
        
