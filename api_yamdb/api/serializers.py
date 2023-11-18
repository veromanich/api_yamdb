from rest_framework import serializers

from reviwes.models import User, Category, Genre, Titles


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
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        # read_only_fields = ('slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=False, many=True)
    #category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    category = CategorySerializer(required=False, many=False)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
