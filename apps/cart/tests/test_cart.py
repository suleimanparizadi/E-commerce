from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.products.models import Product, Category, CPU
from apps.cart.models.cart import Cart, CartItem

User = get_user_model()


class CartViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        
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
        
        self.out_of_stock_product = Product.objects.create(
            category=self.category,
            cpu=self.cpu,
            brand='HP',
            name='HP Pavilion',
            slug='hp-pavilion',
            description='Budget laptop',
            price=25000000,
            stock=0,  # Out of stock
            ram=8,
            storage=256,
            on_board_gpu=True,
            gpu='Intel UHD',
            touch_screen=False,
            display_size=14.0,
            thumbnail='products/thumbnails/test3.jpg'
        )
        
        # URLs
        self.cart_detail_url = reverse('cart:cart_detail')
        self.add_item_url = reverse('cart:add_item')
        self.clear_cart_url = reverse('cart:clear_cart')
    
    def _get_item_url(self, item_id):
        """Helper: Get URL for specific cart item."""
        return reverse('cart:cart_item', kwargs={'item_id': item_id})
    
    def _authenticate(self, user):
        """Helper: Authenticate a user."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
    
    def _clear_auth(self):
        """Helper: Remove authentication."""
        self.client.credentials()
    
    def _add_item(self, product_slug, quantity=1):
        """Helper: Add item to cart."""
        return self.client.post(
            self.add_item_url,
            {'product_slug': product_slug, 'quantity': quantity},
            format='json'
        )
    
    def _create_cart_with_items(self, user=None, session_key=None):
        """Helper: Create a cart with items for testing."""
        if user:
            cart = Cart.objects.create(user=user)
        else:
            cart = Cart.objects.create(session_key=session_key or 'test_session_key')
        
        item1 = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        item2 = CartItem.objects.create(
            cart=cart,
            product=self.product2,
            quantity=1
        )
        
        return cart, item1, item2
    
    def _create_session(self):
        """Helper: Create a session for guest user."""
        self.client.post('/')  # Initialize session
        session = self.client.session
        session.save()
        return session.session_key