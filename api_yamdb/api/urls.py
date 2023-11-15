from django.urls import include, path
from rest_framework import routers

from api.views import (
    APISignup,
    CategoryViewSet,
    GenreViewSet,
    GetToken,
    TitlesViewSet,
    UserViewSet,
)


router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='get_token'),
    path('v1/', include(router_v1.urls)),
]
