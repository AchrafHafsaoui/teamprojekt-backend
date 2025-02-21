from django.urls import path

from .views import CreateNewParking, EditParking, GetAllParkings, RemoveParking

urlpatterns = [
    path('create/', CreateNewParking.as_view(), name='CreateNewParking'),
    path('get/', GetAllParkings.as_view(), name='GetAllParkings'),
    path('edit/', EditParking.as_view(), name='EditParking'),
    path('delete/', RemoveParking.as_view(), name='RemoveParking'),
]