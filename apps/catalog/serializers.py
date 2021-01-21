from rest_framework import serializers



class BaseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)