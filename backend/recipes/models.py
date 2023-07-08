from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.constraints import CheckConstraint, UniqueConstraint

from api.constants import (
    MAX_VALUE_AMOUNT, MAX_VALUE_COOKING_TIME, MIN_VALUE_AMOUNT,
    MIN_VALUE_COOKING_TIME
)
from api.validators import validate_hex_color

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название',
        help_text='Уникальное поле. Длина не более 200 символов.',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=(validate_hex_color,),
        verbose_name='Цвет в HEX',
        help_text='Уникальное поле. Код цвета в HEX.',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг',
        help_text=('Уникальное поле. Длина не более 200 символов. Допустимые '
                   'символы: -, _, латинские буквы, цифры.'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Длина не более 200 символов.',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Длина не более 200 символов.',
    )

    class Meta:
        ordering = ('name',)
        constraints = (
            UniqueConstraint(fields=('name', 'measurement_unit',),
                             name='unique_name_measurement_unit'),
        )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Автор рецепта (пользователь).',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Длина не более 200 символов.',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        help_text='Список ингредиентов рецепта.',
    )
    tags = models.ManyToManyField(
        Tag, through='TagRecipe',
        related_name='recipes',
        verbose_name='Список тегов',
        help_text='Список тегов рецепта.',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Картинка',
        help_text='Картинка (при передаче через API закодированная в Base64).',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта',
    )
    cooking_time = models.SmallIntegerField(
        validators=(
            MinValueValidator(MIN_VALUE_COOKING_TIME),
            MaxValueValidator(MAX_VALUE_COOKING_TIME),
        ),
        verbose_name='Время приготовления',
        help_text=(f'Время приготовления в минутах. Минимальное значение - '
                   f'{MIN_VALUE_COOKING_TIME}. Максимальное значение - '
                   f'{MAX_VALUE_COOKING_TIME}.'),
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Дата добавления рецепта',
        help_text='Дата добавления рецепта. Заполняется автоматически.',
    )

    class Meta:
        ordering = ('-pub_date', )
        constraints = (
            UniqueConstraint(fields=('author', 'name',),
                             name='unique_author_recipe'),
        )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class TagRecipe(models.Model):
    """Модель для связи тегов и рецептов."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='ID рецепта.',
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='ID тега.',
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('recipe', 'tag',),
                             name='unique_recipe_tag'),
        )
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецептов'

    def __str__(self) -> str:
        return f'{self.recipe} {self.tag}'


class IngredientRecipe(models.Model):
    """Модель для связи ингредиентов и рецептов."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredientrecipe',
        verbose_name='Рецепт',
        help_text='ID рецепта.',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT,
        related_name='ingredientrecipe',
        verbose_name='Ингредиент',
        help_text='ID ингредиента.',
    )
    amount = models.IntegerField(
        validators=(
            MinValueValidator(MIN_VALUE_AMOUNT),
            MaxValueValidator(MAX_VALUE_AMOUNT),
        ),
        verbose_name='Количество ингредиента в рецепте',
        help_text=(f'Количество ингредиента в рецепте. Минимальное значение - '
                   f'{MIN_VALUE_AMOUNT}. Максимальное значение - '
                   f'{MAX_VALUE_AMOUNT}.'),
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('recipe', 'ingredient',),
                             name='unique_recipe_ingredient'),
        )
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self) -> str:
        return f'{self.recipe} {self.ingredient}'


class Favorite(models.Model):
    """Модель для избранных рецептов пользователей."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='ID пользователя.',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='ID рецепта.',
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('user', 'recipe',),
                             name='unique_favorite_recipe'),
        )
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'


class Subscription(models.Model):
    """Модель для подписок пользователей."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик',
        help_text='ID подписчика.',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Автор',
        help_text='ID автора.',
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('user', 'author',),
                             name='unique_subscription'),
            CheckConstraint(check=~models.Q(user=models.F('author')),
                            name='user_not_author')
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user} {self.author}'


class ShoppingCart(models.Model):
    """Модель для списков покупок пользователей."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        help_text='ID пользователя.',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт в списке покупок',
        help_text='ID рецепта в списке покупок.',
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            UniqueConstraint(fields=('user', 'recipe',),
                             name='unique_shopping_cart'),
        )
        verbose_name = 'Рецепт из Списка покупок'
        verbose_name_plural = 'Рецепты из Списков покупок'

    def __str__(self) -> str:
        return f'{self.user} {self.recipe}'
