from django.urls import path
from .views import AddUserView, LoginView, RefreshAccessTokenView, IsAuthView

urlpatterns = [
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('access_token/refresh/', RefreshAccessTokenView.as_view(), name='RefreshAccessTokenView'),
    path('is_auth/', IsAuthView.as_view(), name='IsAuthView'),
]
