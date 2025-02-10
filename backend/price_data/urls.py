from django.urls import path
from .views import get_entsoe_data  # Import the correct function-based view

urlpatterns = [
    path('entsoe-data/', EntsoeDataView.as_view(), name='entsoe-data'),
]