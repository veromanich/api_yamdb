from django.urls import include, path
from rest_framework import routers

from api.views import UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
