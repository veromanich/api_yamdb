from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.response import Response

from api.filters import TitileFilter
from api.permissions import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitlesSerializerRead, TitlesSerializerWrite)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitileFilter
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def create(self, request, *args, **kwargs):
        write_serializer = TitlesSerializerWrite(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        obj = write_serializer.save()
        headers = self.get_success_headers(write_serializer.data)
        read_serializer = TitlesSerializerRead(obj)
        return Response(read_serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_serializer = TitlesSerializerWrite(instance,
                                                 data=request.data,
                                                 partial=partial)
        write_serializer.is_valid(raise_exception=True)
        obj = obj = write_serializer.save()
        read_serializer = TitlesSerializerRead(obj)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(read_serializer.data)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializerRead
        else:
            return TitlesSerializerWrite


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly,
    )
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_queryset = Review.objects.filter(title=title_id)
        return review_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly,
    )
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
