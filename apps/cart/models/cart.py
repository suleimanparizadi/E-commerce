from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.products import Product
from django.core.validators import MinValueValidator, MaxValueValidator



User = get_user_model()



class Cart(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                 blank=True, null=True , related_name='cart')
    
    session_key = models.CharField(max_length=40, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at}"
    


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])

  
    # make sure on a cart there is not more then a one product(if it is then raise the quantity)
    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name = 'unique_cart_product' 
                )]
        

    def __str__(self):
        return f"{self.cart} - {self.product} - {self.quantity}"