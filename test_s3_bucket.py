from django.core.files.base import ContentFile
from apps.products.models import Product, Category, CPU

category = Category.objects.first()
cpu = CPU.objects.first()

product = Product.objects.create(
    category=category, cpu=cpu,
    name='S3 Final Test 3', brand='Test',
    slug='s3-final-test-3', price=10000000,
    ram=8, storage=256, gpu='Integrated',
    thumbnail=ContentFile(b'fake image', 'test_product.jpg'),
)

print(product.thumbnail.url)