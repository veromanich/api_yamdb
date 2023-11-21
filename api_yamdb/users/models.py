from django.contrib.auth.models import AbstractUser
from django.db import models

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
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[validate_username],
    )
    email = models.EmailField(
        'Электронная почта', max_length=254, unique=True, null=True
    )
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=40,
        blank=False,
        null=True,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username[:TEXT_REPRESENTATION_LENGTH]
