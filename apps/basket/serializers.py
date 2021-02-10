from rest_framework import serializers 
from .models import Basket, ProductArray
from catalog.serializers import NestedProductSerializer



class BasketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Basket
        fields = (
            'id',
            'owner',
            'products',
            'status'
        )
        read_only_fields = ('id', 'owner')



class ProductArraySerializer(serializers.ModelSerializer):
    product = NestedProductSerializer()

    class Meta:
        model = ProductArray
        fields = (
            'id',
            'product',
            'basket',
            'quantity'
        )
        read_only_fields = ('id',)