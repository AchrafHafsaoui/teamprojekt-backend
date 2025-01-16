from django.urls import path
from .views import EntsoeDataView

urlpatterns = [
    path('api/entsoe-data/', EntsoeDataView.as_view(), name='entsoe-data'),
]
