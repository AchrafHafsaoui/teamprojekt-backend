from django.urls import path
from .views import SomeProtectedView

urlpatterns = [
    path('token_role/', SomeProtectedView.as_view(), name='SomeProtectedView'),
]