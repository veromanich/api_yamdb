from django.conf import settings
from rest_framework import serializers

from users.models import User
from users.validators import validate_username


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, username):
        return validate_username(username)


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        required=True,
    )
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        return validate_username(username)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
