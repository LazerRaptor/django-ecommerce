from rest_framework import serializers 

from catalog.serializers import ProductSerializer
from .models import Basket, BasketLine



class BasketLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = BasketLine
        fields = (
            'product', 
            'quantity',
        )


class BasketWritableNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketLine
        fields = (
            'product',
            'quantity',
        )
    
    def create(self, validated_data):
        basket = validated_data.pop('basket')
        product = validated_data.pop('product')
        quantity = validated_data.pop('quantity')
        return basket.add(
            product_id=product.id,
            quantity=quantity
        )



class BasketSerializer(serializers.ModelSerializer):
    items = BasketLineSerializer(many=True)

    class Meta:
        model = Basket
        fields = ('id', 'owner', 'items')
        read_only_fields = ('id', 'owner')




