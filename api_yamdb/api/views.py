from django.shortcuts import get_object_or_404
from rest_framework import viewssets
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination


from api.permissions import ReadOnly
from api.serializers import (UserSerializer,
                             CategorySerializer,
                             CommentSerializer,
                             GenreSerializer,
                             TitlesSerializer,
                             ReviewSerializer)
from reviwes.models import (User,
                            Category,
                            Genre,
                            Titles,

                            )

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (ReadOnly,)
    # permission_classes = [ReadOnly or permissions.IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Titles, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer