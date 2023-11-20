from rest_framework import serializers

from reviwes.models import Comment, Category, Genre, Titles, Review

from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        #read_only_fields = ('slug',)
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')


class TitlesSerializerRead(TitlesSerializer):
    category = CategorySerializer(required=False)
    genre = GenreSerializer(required=False, many=True)


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
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
