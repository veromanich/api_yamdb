from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Category, Genre)
class CategoryGenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'review',
        'pub_date',
    )
    search_fields = ('author',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'author',
        'title',
        'score',
    )
    search_fields = ('author',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'get_genre',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category',)
    list_display_links = None
    list_editable = ('category',)
