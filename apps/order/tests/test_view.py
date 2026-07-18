from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.products.models import Product, Category, CPU
from apps.cart.models.cart import Cart, CartItem
from apps.order.models.order_model import Order, OrderItem




User = get_user_model()


class OrderViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        # Create users
        self.user = User.objects.create_user(
            phone_number='09123456789',
            first_name='Ali',
            last_name='Mohammadi',
            password='testpass123',
            email='ali@example.com'
        )
        
        self.other_user = User.objects.create_user(
            phone_number='09987654321',
            first_name='Sara',
            last_name='Hosseini',
            password='testpass456',
            email='sara@example.com'
        )
        
        # Create category
        self.category = Category.objects.create(
            name='Laptop',
            slug='laptop'
        )
        
        # Create CPU
        self.cpu = CPU.objects.create(
            manufacturer=CPU.Manufacturer.INTEL,
            series='Core i7',
            model='13700H',
            cores=14
        )
        
        # Create products
        self.product = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            brand='Asus',
            name='Asus ROG Gaming Laptop',
            slug='asus-rog-gaming-laptop',
            description='A powerful gaming laptop',
            price=50000000,
            stock=10,
            ram=16,
            storage=512,
            on_board_gpu=False,
            gpu='RTX 4060',
            touch_screen=False,
            display_size=15.6,
            thumbnail='products/thumbnails/test.jpg'
        )
        
        self.product2 = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            brand='Dell',
            name='Dell XPS 15',
            slug='dell-xps-15',
            description='Premium ultrabook',
            price=45000000,
            stock=5,
            ram=16,
            storage=512,
            on_board_gpu=True,
            gpu='Intel Iris Xe',
            touch_screen=True,
            display_size=15.0,
            thumbnail='products/thumbnails/test2.jpg'
        )
        
        # Create cart with items for user
        self.cart = Cart.objects.create(user=self.user)
        
        self.cart_item1 = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        
        self.cart_item2 = CartItem.objects.create(
            cart=self.cart,
            product=self.product2,
            quantity=1
        )
        
        # Create existing order for testing detail/list views
        self.order = Order.objects.create(
            user=self.user,
            status=Order.Status.PENDING,
            shipping_city='Tehran',
            shipping_address='Valiasr Street, No 123',
            shipping_postal_code='1234567890',
            total_amount=145000000  # 2*50M + 1*45M
        )
        
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=50000000
        )
        
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=1,
            price_at_purchase=45000000
        )
        
        # URLs
        self.checkout_url = reverse('order:checkout')
        self.list_orders_url = reverse('order:list_orders')
        self.order_detail_url = reverse('order:detail_order', kwargs={'order_id': self.order.id})
    
    def _authenticate(self, user):
        """Helper: Authenticate a user."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
    
    def _clear_auth(self):
        """Helper: Remove authentication."""
        self.client.credentials()
    
    def _get_checkout_data(self):
        """Helper: Get valid checkout data."""
        return {
            'shipping_city': 'Tehran',
            'shipping_address': 'Valiasr Street, No 456',
            'shipping_postal_code': '0987654321'
        }
    



    def test_checkout_success(self):

        self._authenticate(self.user)

        data = self._get_checkout_data()
        response = self.client.post(self.checkout_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.filter(user=self.user).last()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_amount, 145000000) 
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
        
        self.product.refresh_from_db()
        self.product2.refresh_from_db()
       
        self.assertEqual(self.product.stock, 8)  
        self.assertEqual(self.product2.stock, 4)


    def test_checkout_unauthorized(self):


        data = self._get_checkout_data()
        response = self.client.post(self.checkout_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    def test_get_user_list_orders(self):

        self._authenticate(self.other_user)
        response = self.client.get(self.list_orders_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data'], [])



    def test_get_detail_order(self):

        self._authenticate(self.user)
        response = self.client.get(self.order_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_clear_cart_after_checkout(self):

        self._authenticate(self.user)

        data = self._get_checkout_data()
        self.client.post(self.checkout_url, data, format='json')

        # check the cart is empty after checkout
        self.assertEqual(self.cart.items.count(), 0)