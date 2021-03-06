from django.contrib import admin
from .models import Basket, BasketLine



class BasketInline(admin.TabularInline):
    model = BasketLine


class BasketAdmin(admin.ModelAdmin):
    inlines = [
        BasketInline,
    ]


admin.site.register(Basket, BasketAdmin)
admin.site.register(BasketLine)
