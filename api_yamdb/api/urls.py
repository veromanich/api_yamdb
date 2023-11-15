from django.urls import include, path
from rest_framework import routers

from api.views import GetToken, APISignup, UserViewSet


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
