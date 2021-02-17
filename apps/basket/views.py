from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .models import Basket, ProductArray
from .serializers import BasketSerializer, ProductArraySerializer



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
            serializer = BasketSerializer(obj)
        else:
            data = {"owner": None}
            serializer = BasketSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class BasketUUIDAPIView(APIView):
    '''
    Handles the case when UUID is provided
    '''
    # TODO: Does it need permission classes? 
    allowed_methods = ['GET', 'DELETE']
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, uuid, format=None):
        user = request.user
        obj = get_object_or_404(Basket.objects.all(), id=uuid)
        
        if obj.owner is not None and obj.owner != request.user:
            raise PermissionDenied
        
        serializer = BasketSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, uuid, format=None):
        obj = get_object_or_404(Basket.objects.all(), id=uuid)
        data = BasketSerializer(obj).data 
        obj.delete()

        return Response(data, status=status.HTTP_200_OK)
        


class ProductArrayDetailAPIView(APIView):
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
        string_repr = obj.__str__()
        obj.delete()
        data = _('{} has been removed'.format(string_repr))

        return Response(data=data, status=status.HTTP_200_OK)



class ProductArrayListAPIView(APIView):
    '''
    Get product arrays associated with a given basket.
    '''
    allowed_methods = ['GET',]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, uuid, format=None):
        qs = ProductArray.objects.filter(basket_id=uuid)
        serializer = ProductArraySerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)