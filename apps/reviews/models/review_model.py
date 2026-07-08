from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.products import Product
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()




class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                 related_name='reviews')
    
    rating = models.PositiveSmallIntegerField(validators=
        [MinValueValidator(1), MaxValueValidator(5)]
        )

    comment = models.CharField(max_length=225, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
            
            # prevents users from reviewing the same product more than once
            constraints = models.UniqueConstraint(
                 fields=['user', 'product'],
                 name='unique_review_product'
            )

            ordering = ['-created_at']



    def __str__(self):
        return f"{self.comment} - {self.product} - {self.user}"

