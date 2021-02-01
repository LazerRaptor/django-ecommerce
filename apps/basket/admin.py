from django.contrib import admin
from .models import Basket, BasketProduct



class BasketProductInline(admin.TabularInline):
    model = BasketProduct


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        BasketProductInline
    ]


admin.site.register(Basket, BasketAdmin)
