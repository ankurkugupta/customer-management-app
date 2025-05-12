


from django.urls import path

from users.views import UserRegistrationView, UserLogoutView

urlpatterns=[
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]