from django.urls import path

from users.apis.user import LogoutAPI, UserRegistrationAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns=[
    path('register/', UserRegistrationAPI.as_view(), name='register'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair_v1'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_v1'),
]