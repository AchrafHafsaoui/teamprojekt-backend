from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ElectricBusViewSet

router = DefaultRouter()
router.register(r'buses', ElectricBusViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
