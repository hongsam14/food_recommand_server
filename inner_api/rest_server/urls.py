"""rest_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers
from food_recommand import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns

import food_recommand.api

app_name = food_recommand

# router = routers.DefaultRouter()
# router.register(r'rest/pick-food', views.pick_foodViewSet, basename='Food')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/pick-food/', views.pickFood),
    # path('', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
