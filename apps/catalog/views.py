from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category
from django_filters import rest_framework as filters
from .serializers import (
    ProductSerializer, CategorySerializer, ProductSlugSerializer) 



class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get',], url_path='content')
    def category_content(self, request, pk=None):
        '''
        Get reverse related products for a given category. If the category is a 
        parent node, we include products that are reverse related to its descendants.
        '''
        try:
            category_obj = Category.objects.get(id=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data="Category not found")
        
        if category_obj.is_leaf_node():
            query = Q(category_id=pk)
        else:
            descendants_id_list = [
                desc.id for desc in category_obj.get_descendants(include_self=True)]
            query = Q(category_id__in=descendants_id_list)

        products = Product.objects.filter(query)
        serializer = ProductSerializer(products, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filterset_class = ProductFilter



class ProductStaticPaths(APIView):
    '''
    Returns a list of slugs, required for Next.js SSG
    '''
    def get(self, request, format=None):
        slugs = Product.objects.slugs()
        serializer = ProductSlugSerializer(slugs)

        return Response(serializer.data, status=status.HTTP_200_OK)

