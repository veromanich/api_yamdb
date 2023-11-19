from django.db import models
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)

from users.models import User


TEXT_REPRESENTATION_LENGTH = 30


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория', max_length=200, blank=False, null=False
    )
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True, max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.name[:TEXT_REPRESENTATION_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр', max_length=256, blank=False, null=False
    )
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True, max_length=50
    )

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
    description = models.TextField()

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

      
class Review(models.Model):
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
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение',
        null=True
    )
    score = models.PositiveIntegerField(
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
    rating = models.IntegerField(default=None, null=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']

    def __str__(self):
        return self.text[:TEXT_REPRESENTATION_LENGTH]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        title = self.title
        reviews = title.reviews.all()
        if reviews:
            sum_of_scores = sum(review.score for review in reviews)
            new_average_rating = sum_of_scores / len(reviews)
        else:
            new_average_rating = None

        if title.average_rating != new_average_rating:
            title.average_rating = new_average_rating
            title.save(update_fields=['average_rating'])
            

class Comment(models.Model):
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

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TEXT_REPRESENTATION_LENGTH]
    
