from django_filters.rest_framework import CharFilter, FilterSet

from reviwes.models import Title


class TitileFilter(FilterSet):
    genre = CharFilter('genre__slug')
    category = CharFilter('category__slug')

    class Meta:
        model = Title
        fields = (
            'category',
            'genre',
            'name',
            'year'
        )
