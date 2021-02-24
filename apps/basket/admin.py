from django.contrib import admin
from .models import Basket, ProductArray



class ProductArrayInline(admin.TabularInline):
    model = ProductArray


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        ProductArrayInline
    ]


admin.site.register(Basket, BasketAdmin)
admin.site.register(ProductArray)
