from django.urls import path

from .views import GetLoginLogs, LogoutView

urlpatterns = [
    path('get/', GetLoginLogs.as_view(), name='GetLoginLogs'),
    path('logout/', LogoutView.as_view(), name='LogoutView'),
]