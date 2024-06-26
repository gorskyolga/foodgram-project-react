# Generated by Django 3.2.3 on 2023-07-08 19:00

import api.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Длина не более 200 символов.', max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Длина не более 200 символов.', max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Количество ингредиента в рецепте. Минимальное значение - 1. Максимальное значение - 100000.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000)], verbose_name='Количество ингредиента в рецепте')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Длина не более 200 символов.', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Картинка (при передаче через API закодированная в Base64).', upload_to='recipes/images/', verbose_name='Картинка')),
                ('text', models.TextField(help_text='Описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.SmallIntegerField(help_text='Время приготовления в минутах. Минимальное значение - 1. Максимальное значение - 10000.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10000)], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, help_text='Дата добавления рецепта. Заполняется автоматически.', verbose_name='Дата добавления рецепта')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Рецепт из Списка покупок',
                'verbose_name_plural': 'Рецепты из Списков покупок',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Уникальное поле. Длина не более 200 символов.', max_length=200, unique=True, verbose_name='Название')),
                ('color', models.CharField(help_text='Уникальное поле. Код цвета в HEX.', max_length=7, unique=True, validators=[api.validators.validate_hex_color], verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(help_text='Уникальное поле. Длина не более 200 символов. Допустимые символы: -, _, латинские буквы, цифры.', max_length=200, unique=True, verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='ID рецепта.', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(help_text='ID тега.', on_delete=django.db.models.deletion.CASCADE, to='recipes.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег рецепта',
                'verbose_name_plural': 'Теги рецептов',
                'ordering': ('id',),
            },
        ),
    ]
