from django.conf.urls import url, include
from rest_framework import routers

from .views import ProductViewSet, MovementViewSet, PartnerViewSet, LocationViewSet

router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = 'Api Inventory'
router.get_api_root_view().cls.__doc__ = 'Inventory Control'
router.register(r'products', ProductViewSet)
router.register(r'movements', MovementViewSet)
router.register(r'partner', PartnerViewSet)
router.register(r'locations', LocationViewSet)


urlpatterns = [
   url(r'^', include(router.urls)),
]
