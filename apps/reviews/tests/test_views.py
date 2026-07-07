from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.products.models import Product, Category, CPU
from apps.reviews.models import Review

User = get_user_model()


class ReviewViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
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
        
        self.admin = User.objects.create_superuser(
            phone_number='09111111111',
            first_name='Admin',
            last_name='System',
            password='adminpass123'
        )
        
        self.category = Category.objects.create(
            name='Laptop',
            slug='laptop'
        )
        
        self.cpu = CPU.objects.create(
            manufacturer=CPU.Manufacturer.INTEL,
            series='Core i7',
            model='13700H',
            cores=14
        )
        
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
        
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment='Very satisfied with this purchase',
        )
        
        self.list_reviews_url = reverse(
            'reviews:list_product_reviews',
            kwargs={'product_slug': self.product.slug}
        )
        self.create_review_url = reverse(
            'reviews:create_product_view',  
            kwargs={'product_slug': self.product.slug}
        )
        self.review_detail_url = reverse(
            'reviews:edit/remove_review',  
            kwargs={'review_id': self.review.id}  
        )
    
    def _authenticate(self, user):
        """Helper: Authenticate a user."""
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}'
        )
    
    def _clear_auth(self):
        """Helper: Remove authentication."""
        self.client.credentials()
    
    def _create_review_data(self, rating=5, comment='Test comment'):
        """Helper: Create valid review data."""
        return {
            'rating': rating,
            'comment': comment
        }
    


    def test_get_review_of_product(self):

        response = self.client.get(self.list_reviews_url)
        product_rating = self.product.reviews.filter(product=self.product).first().rating
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(product_rating, 4)



    def test_get_review_for_none_exist_product(self):

        url = reverse('reviews:list_product_reviews',
            kwargs={'product_slug': 'Mac_book'})
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    


    def test_create_review(self):

        self._authenticate(self.other_user)
        data = self._create_review_data(rating=4, comment="Good laptop")
        response = self.client.post(self.create_review_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_duplicate_review(self):   

        self._authenticate(self.user)
        data = self._create_review_data(rating=4, comment="Good laptop")
        response = self.client.post(self.create_review_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
    def test_create_review_unauthenticated(self):

        
        data = self._create_review_data(rating=4, comment="Good laptop")
        
        response = self.client.post(self.create_review_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_review(self):

        self._authenticate(self.user)
        data = self._create_review_data(rating=2, comment="Not so good laptop")
        response = self.client.patch(self.review_detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_delete_review(self):

        self._authenticate(self.user)
        
        response = self.client.delete(self.review_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_update_review_by_not_owner(self):

        self._authenticate(self.other_user)
        data = self._create_review_data(rating=2, comment="Not so good laptop")
        response = self.client.patch(self.review_detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_review_by_not_owner(self):

        self._authenticate(self.other_user)
        
        response = self.client.delete(self.review_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_update_review_by_admin(self):

        self._authenticate(self.admin)
        data = self._create_review_data(rating=2, comment="Not so good laptop")
        response = self.client.patch(self.review_detail_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_review_by_admin(self):

        self._authenticate(self.admin)
        
        response = self.client.delete(self.review_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


