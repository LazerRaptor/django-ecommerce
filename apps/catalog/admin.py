from django.contrib import admin

from .models import ModelNode, Bike, Hat, Book, Category


admin.site.register(ModelNode)
admin.site.register(Bike)
admin.site.register(Hat)
admin.site.register(Book)
admin.site.register(Category)