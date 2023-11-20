from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitlesSerializerRead,
    TitlesSerializerWrite,
)
from api.permissions import (
    IsAdminModeratorOwnerOrReadOnly,
    IsAdminOnly,
    IsAdminOrReadOnly,
)
from reviwes.models import Category, Genre, Titles

from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class CategoryViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    # permission_classes = (IsAdminOnly,)
    # permission_classes = [IsAdminOnly or permissions.IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitileFilter(django_filters.FilterSet):
    cities = django_filters.CharFilter(
        name='genre__slug',
        lookup_type='contains', lookup_field='slug'
    )

    class Meta:
        model = Titles
        fields = ('category__slug', 'genre', 'name', 'year', )


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filter_fields = ('category__slug', 'genre', 'name', 'year',)
    filter_class = TitileFilter
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializerRead
        else:
            return TitlesSerializerWrite
