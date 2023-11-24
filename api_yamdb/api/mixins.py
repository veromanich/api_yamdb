from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet

from rest_framework.pagination import PageNumberPagination

from api.permissions import IsAdminOrReadOnly
from rest_framework.filters import SearchFilter


class CreateListDestroySearchMixin(
    DestroyModelMixin,
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
