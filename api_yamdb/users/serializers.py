from rest_framework import serializers

from api_yamdb.settings import (
    EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
)
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
    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, username):
        return validate_username(username)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=USERNAME_MAX_LENGTH,
        required=True,
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
