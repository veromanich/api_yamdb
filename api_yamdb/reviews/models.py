from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from api_yamdb.settings import TEXT_REPRESENTATION_LENGTH


class BaseMeta:
    ordering = ['id']


class BaseAbstractModel(models.Model):
    class Meta(BaseMeta):
        abstract = True

    def __str__(self):
        return str(self)[:TEXT_REPRESENTATION_LENGTH]


class BaseDictModel(models.Model):
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return str(self.name)[:TEXT_REPRESENTATION_LENGTH]


class Category(BaseDictModel):
    name = models.CharField(
        verbose_name='Категория', max_length=256, null=True
    )

    class Meta(BaseDictModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(BaseDictModel):
    name = models.CharField(
        verbose_name='Жанр', max_length=256
    )

    class Meta(BaseDictModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=256,
        unique=True,
        blank=False,
        null=False,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска',
        validators=(
            MaxValueValidator(date.today().year),
        ),
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
        ordering = ['-id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'

    def __str__(self):
        return f'{self.title} {self.genre}'[:TEXT_REPRESENTATION_LENGTH]


class Review(BaseAbstractModel):
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
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

    class Meta(BaseMeta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']

    @property
    def owner(self):
        return self.author


class Comment(BaseAbstractModel):
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='oтзыв',
    )

    class Meta(BaseMeta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    @property
    def owner(self):
        return self.author
