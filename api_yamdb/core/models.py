from django.conf import settings
from django.db import models

from users.models import User


class BaseDictModel(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=settings.NAME_MAX_LENGTH,
        null=True,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.TEXT_REPRESENTATION_LENGTH]


class BaseTextPublishModel(models.Model):
    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.TEXT_REPRESENTATION_LENGTH]

    @property
    def owner(self):
        return self.author
