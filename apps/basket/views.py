from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .models import Basket, ProductArray
from .serializers import BasketSerializer, ProductArraySerializer, Product


# FIXME: These views are screaming for refactoring. 
# TODO: Add tests, they are needed here.

class BasketUnknownAPIView(APIView):
    '''
    Attempt to get the most recent basket for an authenticated user, 
    if fails create a new one.
    '''
    allowed_methods = ['GET',]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, format=None):
        user = request.user
        if user.is_authenticated:
            qs = user.baskets.filter(status='open')
            obj = qs.order_by('-updated').first()
            if obj is None:
                obj = Basket.objects.create(owner_id=user.id)
            serializer = BasketSerializer(obj)
        else:
            obj = Basket.objects.create(owner=None)
            serializer = BasketSerializer(obj)

        return Response(serializer.data, status=status.HTTP_200_OK)
        


class BasketUUIDAPIView(APIView):
    '''
    Handles the case when UUID is provided
    '''
    # TODO: add nested arrays of products to serialized carts 
    allowed_methods = ['GET', 'DELETE']
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, uuid, format=None):
        user = request.user if request.user.is_authenticated else None
        obj = get_object_or_404(Basket.objects.all(), id=uuid)
        
        if obj.owner is not None and obj.owner != request.user:
            raise PermissionDenied
        
        qs = ProductArray.objects.filter(basket_id=uuid)
        serializer = ProductArraySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, uuid, format=None):
        obj = get_object_or_404(Basket.objects.all(), id=uuid)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

# FIXME: terrible name
class ProductArrayDetailAPIView(APIView):
    '''
    Manage a single ProductArray instance
    '''
    allowed_methods = ['PUT', 'DELETE']
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    
    def put(self, request, id, format=None):
        quantity = request.data.get('qty', 1)
        obj = get_object_or_404(ProductArray.objects.all(), id=id)
        serializer = ProductArraySerializer(instance=obj, data={"quantity": quantity})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        obj = get_object_or_404(
            ProductArray.objects.all(),
            id=id
        )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# FIXME: terrible name
# TODO: Need tests
class ProductArrayListAPIView(APIView):
    '''
    Get a list of ProductArray instances associated with a given basket.
    '''
    allowed_methods = ['POST',]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]


    
    @transaction.atomic
    def post(self, request, format=None):
        user = request.user if request.user.is_authenticated else None
        basket_id = request.data.get('basket') 
        product_id = request.data.get('product')

        if product_id is None:
            return Response(_('ID for Product instance is not provided'), status=status.HTTP_400_BAD_REQUEST)
        
        if basket_id is None:
            basket = Basket.objects.create(owner=user)
            basket_id = basket.id

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                data=_('Product not found'),
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            basket = Basket.objects.get(id=basket_id)
        except Basket.DoesNotExist:
            return Response(
                data=_('Basket is not found, whats going on?'), 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # check if item has already been added
        if ProductArray.objects.filter(
            Q(product=product_id) & Q(basket=basket_id)).exists():
            return Response(data=_('This item is already in the cart'), status=status.HTTP_200_OK)

        data = {
            'basket': basket_id, 
            'product': product_id, 
        }
        serializer = ProductArraySerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
           