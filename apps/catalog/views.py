from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.decorators import action
from .models import Product, Category
from django_filters import rest_framework as filters
from .serializers import (
    ProductSerializer, CategorySerializer, ProductSlugSerializer) 

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'featured', 'min_price', 'max_price']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    lookup_field = 'slug'

    def list(self, request, format=None):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug, format=None):
        queryset = Category.objects.all()
        obj = get_object_or_404(queryset, slug=slug)
        serializer = CategorySerializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['get',], url_path='content')
    def category_content(self, request, slug, format=None):
        '''
        Get reverse related products for a given category. If the category is a 
        parent node, we include products that are reverse related to its descendants.
        '''
        category_obj = get_object_or_404(Category, slug=slug)
        
        if category_obj.is_leaf_node():
            query = Q(category_id=category_obj.id)
        else:
            descendants_id_list = [
                desc.id for desc in category_obj.get_descendants(include_self=True)
            ]
            query = Q(category_id__in=descendants_id_list)

        products = Product.objects.filter(query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryTreeView(APIView):
    '''
    Returns all categories as a tree view
    '''
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [IsAuthenticatedOrReadOnly,]

    @staticmethod
    def build_tree(nodes):
        # FIXME: This is terrible

        def traverse(nodes):
            tree = []
            for node in nodes:
                d = node.copy()
                children = [x for x in nodes if x['parent'] == node['id']]
                children = traverse(children)
                d['children'] = children
                tree.append(d)
            return tree 

        def remove_parent(nodes):
            for n in nodes:
                n.pop("parent")
                if len(n["children"]) > 0:
                    remove_parent(n["children"])
            return nodes

        nodes = traverse(nodes)
        tree = [n for n in nodes if n['parent'] is None]

        return remove_parent(tree)
            
    
    def get(self, request, format=None):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        tree = self.build_tree(serializer.data)
        return Response(tree, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    filterset_class = ProductFilter


class ProductStaticPaths(APIView):
    '''
    Returns a list of slugs, required for Next.js SSG
    '''
    renderers = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, format=None):
        qs = Product.objects.slugs()

        return Response(qs, status=status.HTTP_200_OK)

