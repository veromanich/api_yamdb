from django.contrib.auth.models import AbstractUser
from django.db import models


TEXT_REPRESENTATION_LENGTH = 30


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField('Роль', max_length=30, default='user', blank=True)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:TEXT_REPRESENTATION_LENGTH]


class Category(models.Model):
    name = models.CharField(verbose_name='Категория',
                            max_length=200,
                            blank=False,
                            null=False)
    slug = models.SlugField(verbose_name='Идентификатор',
                            unique=True,
                            max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class Genre(models.Model):
    name = models.CharField(verbose_name='Жанр',
                            max_length=256,
                            blank=False,
                            null=False)
    slug = models.SlugField(verbose_name='Идентификатор',
                            unique=True,
                            max_length=256)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class Titles(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=256,
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

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ['-id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class GenreTitle(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'жанры произведений'

    def __str__(self):
        return f'{self.title} {self.genre}'[:TEXT_REPRESENTATION_LENGTH]
