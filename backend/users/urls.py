from django.urls import path
from .views import AddUserView, GetUsersView, LoginView, RefreshAccessTokenView, IsAuthView, UpdateInfo, UpdateRole

urlpatterns = [
    path('add_user/', AddUserView.as_view(), name='add_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('access_token/refresh/', RefreshAccessTokenView.as_view(), name='RefreshAccessTokenView'),
    path('is_auth/', IsAuthView.as_view(), name='IsAuthView'),
    path('get_all_users/', GetUsersView.as_view(), name='GetUsersView'),
    path('update/info', UpdateInfo.as_view(), name='UpdateInfo'),
    path('update/role', UpdateRole.as_view(), name='UpdateRole'),
]
