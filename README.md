from catalog.models import Book
from basket.models import Basket
from warehouse.models import StockRecord


dic = {
    'title': 'Historia',
    'author': 'Herodotus',
    'price': 19.99,
    'length': 320,
    'book_format': 'H',
}


book = Book.objects.create(**dic)
book.save()

rec = StockRecord.objects.create('delta')



# Do we need a generic relationship between StockRecord and AbstractProduct's children? 

class AbstractProduct: 
    pass 


class Book:
    pass


class StockRecord: 
    basket = models.ForeignKey(Basket)
    product = GenericForeignKey()


class Basket:
    STATUS_CHOICES = (...)
    status = models.CharField(choices=STATUS_CHOICES) 


# How to handle abstract inheritance? 
1. When we need a list of instances, we can omit model-specific fields. We need only general info. 
2. So we can use `values()` or `values_list()` method to get multiple querysets with common fields (from abstract model).
3. Since fields are common, we can use UNION to turn it into a single queryset. And then treat it as usual.  