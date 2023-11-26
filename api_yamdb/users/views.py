from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdminOnly
from users.models import User
from users.serializers import (GetTokenSerializer,
                               SignupSerializer,
                               UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def profile(self, request):
        user = request.user
        serializer = UserSerializer(user)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        try:
            user, _ = User.objects.get_or_create(
                email=email, username=username
            )
        except IntegrityError:
            incorrect_value = {}
            if User.objects.filter(username=username):
                incorrect_value['username'] = ['username уже занят']
            if User.objects.filter(email=email):
                incorrect_value['email'] = ['email уже занят']
            return Response(
                incorrect_value,
                status=status.HTTP_400_BAD_REQUEST,
            )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='YaMDb регистрация',
            message=f'Код подтверждения {confirmation_code}',
            from_email=settings.PROJECT_EMAIL,
            recipient_list=[user.email],
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = str(AccessToken.for_user(user))
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )
