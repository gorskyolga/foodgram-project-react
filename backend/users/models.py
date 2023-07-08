from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import validate_username


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Обязательное поле. Не более 254 символов.',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,),
        verbose_name='Уникальный юзернейм',
        help_text=('Обязательное поле. Не более 150 символов. Допустимые '
                   'символы: латинские буквы, цифры и символы .+-_@.'),
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Обязательное поле. Не более 150 символов.',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Обязательное поле. Не более 150 символов.',
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Обязательное поле. Не более 150 символов.',
    )

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name',)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
