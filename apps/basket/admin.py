from django.contrib import admin
from .models import Basket
from warehouse.models import StockRecord



class StockRecordInline(admin.TabularInline):
    model = StockRecord


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        StockRecordInline
    ]


admin.site.register(Basket, BasketAdmin)
