from rest_framework import serializers
from .models import Product, Category, ProductImage


# TODO: Check out https://github.com/dbrgn/drf-dynamic-fields to refactor serializers for Product model. 

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ProductImage
        fields = (
            'id',
            'product', 
            'src', 
            'alt', 
            'is_showcase'
        )



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'slug',
            'price',
            'description',
            'category',
            'images',
            'featured',
            'extra'
        )


class NestedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product 
        fields = (
            'id',
            'title',
            'slug',
            'price',
            'description'
        )



class ProductSlugSerializer(serializers.Serializer):
    slug = serializers.SlugField(allow_blank=False)

    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'parent')
    