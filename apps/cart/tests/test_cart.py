from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.products.models import Product, Category, CPU
from apps.cart.services.cart_service import CartService

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
            stock=2,
            ram=16,
            storage=512,
            on_board_gpu=True,
            gpu='Intel Iris Xe',
            touch_screen=True,
            display_size=15.0,
            thumbnail='products/thumbnails/test2.jpg'
        )
        
       
        
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
    
    def _create_session(self):
        """Helper: Create a session for guest user."""
        self.client.post('/')  # Initialize session
        session = self.client.session
        session.save()
        return session.session_key
    


    def test_get_cart_authenticated(self):

        self._authenticate(self.user)
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)
        self._add_item(product_slug='dell-xps-15', quantity=1)
        
        response = self.client.get(self.cart_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)



    def test_get_cart_unauthenticated(self):

        
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=1)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)





    def test_increments_existing_item(self):

        self._authenticate(self.user)
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=1) 

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        item = response.data['items'][0]
        self.assertEqual(item['quantity'], 3)


    def test_exceeds_stock_item(self):

        response = self._add_item(product_slug='dell-xps-15', quantity=4)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      



    def test_exceeds_limitation_add(self):

        response = self._add_item(product_slug='asus-rog-gaming-laptop', quantity=8)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      




    def test_update_cart_items(self):

        self._authenticate(self.user)
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)
        
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        item = response.data['items'][0]
        self.assertEqual(item['quantity'], 2)

       

        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        item = response.data['items'][0]
        self.assertEqual(item['quantity'], 4)


        
       


    def test_remove_cart_items(self):

        self._authenticate(self.user)
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=1)
        self._add_item(product_slug='dell-xps-15', quantity=1)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        item_id = response.data['items'][0]['id']
       
        deleting = self.client.delete(reverse('cart:cart_item', kwargs={'item_id':item_id}))
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 1)
        self.assertTrue(deleting)


    
    def test_clear_cart(self):
        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)
        self._add_item(product_slug='dell-xps-15', quantity=1) 

        response = self.client.delete(self.clear_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response)



    def test_merge_carts(self):
        
        self._clear_auth()

        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=3)
        
        self._add_item(product_slug='dell-xps-15', quantity=1)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        item1 = response.data['items'][0]
        self.assertEqual(item1['quantity'], 3)
        item2 = response.data['items'][1]
        self.assertEqual(item2['quantity'], 1)

        session_key = self.client.session.session_key
        self._authenticate(self.user)
        CartService.merge_carts(session_key=session_key, user=self.user)


        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=2)
        self._add_item(product_slug='dell-xps-15', quantity=1)



        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        item1 = response.data['items'][0]
        item2 = response.data['items'][1]

        self.assertEqual(item1['quantity'], 5)
        self.assertEqual(item2['quantity'], 2)

    



    def test_merge_carts_caps_at_max(self):

        self._clear_auth()

        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=3)
        
        self._add_item(product_slug='dell-xps-15', quantity=1)

        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        item1 = response.data['items'][0]
        self.assertEqual(item1['quantity'], 3)
        item2 = response.data['items'][1]
        self.assertEqual(item2['quantity'], 1)

        session_key = self.client.session.session_key
        self._authenticate(self.user)


        self._add_item(product_slug='asus-rog-gaming-laptop', quantity=5)
        self._add_item(product_slug='dell-xps-15', quantity=1)


        CartService.merge_carts(session_key=session_key, user=self.user)

        
        response = self.client.get(self.cart_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)
        item1 = response.data['items'][0]
        item2 = response.data['items'][1]

        # check the max order will be set to 5 if its more then 5
        self.assertEqual(item1['quantity'], 5)
        self.assertEqual(item2['quantity'], 2)
