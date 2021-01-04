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



### TODO: 
1. add tests for TreeNode manager
2. add get_descendants() & get_ancestors() methods to the Node model
3. add get_queryset() method to the TreeNode manager and the likes. 