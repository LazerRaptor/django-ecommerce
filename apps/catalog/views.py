from rest_framework import viewsets
from .serializers import BaseSerializer
from .models import Bike, Book
from itertools import chain


# values = ['title', 'slug', 'price']
# qs1 = Book.objects.values(*values)
# qs2 = Bike.objects.values(*values)
# qs = qs1.union(qs2)


class ProductViewset(viewsets.ViewSet):
    serializer_class = BaseSerializer
    queryset = Bike.objects.all()