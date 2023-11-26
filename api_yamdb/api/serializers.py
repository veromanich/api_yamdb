from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


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
    rating = serializers.SerializerMethodField(
        read_only=True,
        default=None
    )
    category = CategorySerializer(required=False, read_only=True)
    genre = GenreSerializer(required=False, many=True, read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'category',
            'description',
            'rating'
        )

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return avg_rating


class TitlesSerializerWrite(TitlesSerializerRead):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    def to_representation(self, instance):
        if isinstance(instance, Title):
            serializer = TitlesSerializerRead(instance)
        else:
            raise Exception('Unexpected object type')
        return serializer.data


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
        request_method = self.context.get('request').method
        title_id = self.context.get('view').kwargs.get('title_id')
        author = self.context.get('request').user
        review = Review.objects.filter(author=author, title=title_id)
        if request_method == 'POST' and review.exists():
            raise serializers.ValidationError('Вы уже оставили отзыв!!!')
        return data
