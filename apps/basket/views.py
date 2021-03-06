from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from .models import Basket, BasketLine
from .serializers import (
    BasketSerializer, BasketWritableNestedSerializer, BasketLineSerializer)



class BasketAPIView(GenericAPIView):
    '''
    Retrieve a basket by id and manipulate with its containing items.
    The containing items are BasketLine model instances. 
    We can use IDs of Product model instances to identify related BasketLine
    instances as they are unique.
    '''
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    lookup_field = 'id'
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()       

    def check_object_permissions(self, request, obj):
        if obj.owner is not None and obj.owner != request.user:
            raise PermissionDenied
        super().check_object_permissions(request, obj)

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'POST':
            return BasketWritableNestedSerializer
        return super().get_serializer_class()
    
    def get(self, request, *args, **kwargs):
        '''
        Get basket object.
        '''
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        '''
        Add item to the basket.
        '''
        basket = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(basket=basket)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        ''' 
        Delete item from the basket.
        '''
        basket_id = kwargs.pop('id')
        product_id = request.data.get('product')
        instance = get_object_or_404(
            BasketLine, 
            basket_id=basket_id, 
            product_id=product_id
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        '''
        Update quantity for the item.
        '''
        product_id=request.data.get('product')
        basket = self.get_object()
        instance = get_object_or_404(basket.items.all(), product_id=product_id)
        serializer = self.get_serializer(
            instance=instance, 
            data={'quantity': request.data.get('quantity')},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



class CreateBasketAPIView(APIView):
    '''
    Give user a new empty basket. 
    '''
    serializer_class = BasketSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request): 
        user = request.user
        if user.is_anonymous:
            user = None
        serializer = get_serializer(data={'owner': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data