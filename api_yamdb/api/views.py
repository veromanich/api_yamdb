from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)

from api.filters import TitileFilter
from api.mixins import CreateListDestroySearchMixin
from api.permissions import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitlesSerializerRead, TitlesSerializerWrite)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(CreateListDestroySearchMixin,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroySearchMixin,):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitileFilter
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitlesSerializerRead
        return TitlesSerializerWrite

    def get_queryset(self):
        queryset = Title.objects.annotate(avg_rating=Avg('reviews__score'))
        return queryset.order_by('year')


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly,
    )
    serializer_class = ReviewSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminModeratorOwnerOrReadOnly,
    )
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
