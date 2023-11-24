from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Category, Genre, Title, Review


class SlugRelatedFieldDisplayObject(serializers.SlugRelatedField):
    def display_value(self, instance):
        return instance


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


class TitlesSerializerRead(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='avg_rating',
        read_only=True,
        default=None
    )
    category = CategorySerializer(required=False, read_only=True)
    genre = GenreSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'genre', 'category', 'description', 'rating')


class TitlesSerializerWrite(TitlesSerializerRead):
    category = SlugRelatedFieldDisplayObject(slug_field='slug', queryset=Category.objects.all())
    genre = SlugRelatedFieldDisplayObject(slug_field='slug', queryset=Genre.objects.all(), many=True)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        existing_review = Review.objects.filter(author=author, title_id=title_id).exists()
        if existing_review and self.context.get('request').method == 'POST':
            raise serializers.ValidationError('Вы уже оставили отзыв!!!')
        return data
