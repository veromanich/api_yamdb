from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    SignupSerializer,
    TitlesSerializer,
    UserSerializer,
)
from api.permissions import ReadOnly
from reviwes.models import Category, Genre, Titles, User

from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        username = serializer.data['username']
        user, _ = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb регистрация',
            message=f'Код подтверждения {confirmation_code}',
            from_email='yamdb@yandex.ru',
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    pass


class CategoryViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
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
