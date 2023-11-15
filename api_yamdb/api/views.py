from rest_framework import viewsets
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination


from api.permissions import ReadOnly
from api.serializers import (UserSerializer,
                             CategorySerializer,
                             GenreSerializer,
                             TitlesSerializer)
from reviwes.models import (User,
                            Category,
                            Genre,
                            Titles
                            )


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


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
