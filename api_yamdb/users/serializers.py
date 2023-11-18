from rest_framework import serializers
from django.core.validators import RegexValidator

from users.models import User


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


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('username "me" запрещён')
        regular_expression_validate = RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='В username присутствуют запрещенные символы',
            code='invalid_username',
        )
        regular_expression_validate(data['username'])
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fiels = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )