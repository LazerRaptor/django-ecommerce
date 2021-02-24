from django.urls import path
from .views import (BasketUnknownAPIView, BasketUUIDAPIView, ProductArrayDetailAPIView, ProductArrayListAPIView)



urlpatterns = [
    path('basket/', BasketUnknownAPIView.as_view()),
    path('basket/<uuid:uuid>/', BasketUUIDAPIView.as_view()),
    path('basket/items/', ProductArrayListAPIView.as_view()),
    path('basket/items/<int:id>/', ProductArrayDetailAPIView.as_view()),
]
