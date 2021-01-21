from rest_framework import routers
from .views import ProductViewset


router = routers.DefaultRouter()
router.register(r'products', ProductViewset)
urlpatterns = router.urls
print(urlpatterns)