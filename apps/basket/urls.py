from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import BasketAPIView, CreateBasketAPIView



urlpatterns = [
    path('basket/', CreateBasketAPIView.as_view()),
    path('basket/<uuid:id>/', BasketAPIView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])