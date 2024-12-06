from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationList

router = DefaultRouter()
router.register(r'stations',StationList)

urlpatterns = [
    path('api/', include(router.urls)),
]
