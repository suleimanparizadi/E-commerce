from django.db import models
from apps.utils.slug_generator import generate_unique_slug
from .category import Category


class Product(models.Model):
    
    
    cpu = models.ForeignKey(
        'CPU',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Basic Info
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, allow_unicode=True)
    description = models.TextField()
    
    # Pricing & Stock
    price = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)
    
    # Specifications
    ram = models.PositiveSmallIntegerField()
    storage = models.PositiveIntegerField()
    on_board_gpu = models.BooleanField(default=False)
    gpu = models.CharField( max_length=50)
    touch_screen = models.BooleanField(default=False)
    display_size = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        null=True,
        blank=True
    )
    
    # Media
    thumbnail = models.ImageField(upload_to='products/thumbnails/%Y/%m/')
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['brand']),
            models.Index(fields=['is_active', 'stock']),
            models.Index(fields=['cpu']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super().save(*args, **kwargs)
    
    @property
    def is_in_stock(self):
        return self.stock > 0

class CPU(models.Model):
    
    class Manufacturer(models.TextChoices):
        INTEL = 'INTEL', 'Intel'
        AMD = 'AMD', 'AMD'
        APPLE = 'APPLE', 'Apple'
    
    manufacturer = models.CharField(max_length=10, choices=Manufacturer.choices)
    series = models.CharField(max_length=100)  
    model = models.CharField(max_length=100)   
    cores = models.PositiveSmallIntegerField()
    
    class Meta:
        verbose_name = 'CPU'
        verbose_name_plural = 'CPUs'
        ordering = ['manufacturer', 'series']
    
    def __str__(self):
        return f"{self.manufacturer} {self.series} {self.model} ({self.cores} cores)"