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



### Notes: 
1. TreeManager needs refactoring