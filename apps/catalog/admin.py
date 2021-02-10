from django.contrib import admin
from .models import Product, Category, ProductImage



class ImageAdminInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_filter = (
        ('category', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('title', 'description') 
    inlines = [
        ImageAdminInline,
    ]



admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ProductImage)