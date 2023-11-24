from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
)
from users.validators import validate_username


TEXT_REPRESENTATION_LENGTH = 30


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    ]

    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        null=False,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        null=False,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=len(max([role[0] for role in ROLE_CHOICES], key=len)),
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:TEXT_REPRESENTATION_LENGTH]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
