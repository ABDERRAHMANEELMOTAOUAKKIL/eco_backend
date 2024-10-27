from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image','slug']

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.SlugRelatedField(
            queryset=Category.objects.all(),
            slug_field='name'  
        )
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'available', 'created_at', 'updated_at', 'image', 'sku', 'category']
