"""
URL configuration for CustomerManagementApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.apis.health_check_apis import ProtectedApi, AllowAllHealthCheckApi

from django.urls import path
from users.views import UserLoginView

schema_view = get_schema_view(
   openapi.Info(
      title="CustomerManagementApp API",
      default_version='v1',
      description="API documentation for CustomerManagementApp",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/health-check/', AllowAllHealthCheckApi.as_view()),
    path('api/v1/protected-view/', ProtectedApi.as_view()),
    path('api/v1/customers/', include('customers.interface.urls')),
    path("api/v1/user/", include('users.urls.api')),
    path('', UserLoginView.as_view(), name='login'),
    path('user/', include('users.urls.view')),
    path('customer/', include('customers.interface.view_urls')),
]





