from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import NAME_MAX_LENGTH
from users.models import User

TEXT_REPRESENTATION_LENGTH = 30


class BaseMeta:
    ordering = ['id']


class BaseAbstractModel(models.Model):
    class Meta(BaseMeta):
        abstract = True

    def __str__(self):
        return str(self)[:TEXT_REPRESENTATION_LENGTH]


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория', max_length=NAME_MAX_LENGTH, null=True
    )
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=NAME_MAX_LENGTH,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=NAME_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
    )
    year = models.IntegerField()
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='titles')
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle',
                                   related_name='titles')
    description = models.TextField(null=True, blank=True,)

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]

    def get_genre(self):
        return ",".join([str(p) for p in self.genre.all()])


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
