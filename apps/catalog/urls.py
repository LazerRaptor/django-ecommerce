from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (
    ProductViewSet, CategoryViewSet, CategoryTreeView, ProductStaticPaths)



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('paths/products', ProductStaticPaths.as_view()),
    path('category-tree/', CategoryTreeView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

urlpatterns += router.urls