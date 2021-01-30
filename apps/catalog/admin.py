from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import ProductTreeNode, Bike, Hat, Book, Category
from warehouse.models import StockRecord



class StockRecordInline(GenericTabularInline):
    model = StockRecord
    fields = ('supplier', 'delta')


class BookAdmin(admin.ModelAdmin):
    inlines = [
        StockRecordInline
    ]

class BikeAdmin(admin.ModelAdmin):
    inlines = [
        StockRecordInline
    ]

class HatAdmin(admin.ModelAdmin):
    inlines = [
        StockRecordInline
    ]


admin.site.register(Bike, BikeAdmin)
admin.site.register(Hat, HatAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category)