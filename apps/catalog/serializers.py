from rest_framework import serializers
from .models import Product, Category



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'price',
            'description',
            'category',
            'featured',
            'extra'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'slug', 'parent')
    