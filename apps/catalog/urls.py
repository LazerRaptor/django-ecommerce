from django.urls import path
from rest_framework import routers
from .views import ProductViewSet, CategoryViewSet, ProductStaticPaths



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('products/static-paths/', ProductStaticPaths.as_view())
]