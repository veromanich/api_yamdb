from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.models import BaseDictModel, BaseTextPublishModel
from reviews.validators import validate_year


class Category(BaseDictModel):

    class Meta(BaseDictModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseDictModel):

    class Meta(BaseDictModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=settings.NAME_MAX_LENGTH,
        unique=True,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=[validate_year],
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    description = models.TextField(null=True, blank=True,)

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ['year']

    def __str__(self):
        return self.name[:settings.TEXT_REPRESENTATION_LENGTH]

    def get_genre(self):
        return ",".join([str(p) for p in self.genre.all()])


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'

    def __str__(self):
        return (
            f'{self.title} {self.genre}'[:settings.TEXT_REPRESENTATION_LENGTH]
        )


class Review(BaseTextPublishModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Oценка',
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )

    class Meta(BaseTextPublishModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review'
            )
        ]


class Comment(BaseTextPublishModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='oтзыв',
    )

    class Meta(BaseTextPublishModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
