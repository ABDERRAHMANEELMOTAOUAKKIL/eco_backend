from django.db import models
from django.db.models import Q

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)  
    
    @classmethod
    def search(cls, query):
        return cls.objects.filter(
            Q(name__icontains=query) 
        )


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()  # Quantity in stock
    available = models.BooleanField(default=True)  # Product availability
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Optional image field
    sku = models.CharField(max_length=100, unique=True)  # Stock Keeping Unit
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)  # Linking with category

    @classmethod
    def search(cls, query):
        return cls.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(available=True)  # Only show available products in search

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']  # Order products by the newest first