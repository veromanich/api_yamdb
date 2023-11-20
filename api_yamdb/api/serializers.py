from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviwes.models import Comment, Category, Genre, Title, Review

from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')


class TitlesSerializerRead(TitlesSerializer):
    category = CategorySerializer(required=False, read_only=True)
    genre = GenreSerializer(required=False, many=True, read_only=True)


class TitlesSerializerWrite(TitlesSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all(), many=True)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
            title=title, author=author
        ).exists():
            raise serializers.ValidationError('Вы уже оставили свой отзыв'
                                              'к этому произведению!')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
