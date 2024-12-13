from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DrivingScheduleViewSet

router = DefaultRouter()
router.register(r'driving-schedule', DrivingScheduleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
