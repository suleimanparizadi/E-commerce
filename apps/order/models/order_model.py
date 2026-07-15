from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.products import Product


User = get_user_model()



class Order(models.Model):


    class Status(models.TextChoices):
        PENDING = 'PENDING', 'pending'
        CONFIRMED = 'CONFIRMED', 'confirmed'
        SHIPPED = 'SHIPPED', 'shipped'
        DELIVERED = 'DELIVERED', 'delivered'
        CANCELED = 'CANCELED' ,'canceled'


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    shipping_city = models.CharField(max_length=125)
    shipping_address = models.TextField()
    shipping_postal_code = models.CharField(max_length=10) 
    total_amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveSmallIntegerField()
    price_at_purchase = models.IntegerField(editable=False)


    class Meta:
        constraints = [models.UniqueConstraint(
        fields=["order", "product"],
        name="unique_order_product",
    )]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"