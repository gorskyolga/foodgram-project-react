import base64
from djoser.serializers import UserSerializer, UserCreateSerializer

from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.constants import (
    MAX_VALUE_AMOUNT, MAX_VALUE_COOKING_TIME, MIN_VALUE_AMOUNT,
    MIN_VALUE_COOKING_TIME, ErrorMessage
)
from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Subscription,
    Tag
)

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя"""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password',
        )
        read_only_field = ('id',)


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей (кроме создания)"""
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        author = get_object_or_404(User, id=obj.id)
        return Subscription.objects.filter(user=user, author=author).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Ingredient.objects.all(),
                fields=('name', 'measurement_unit'),
                message=ErrorMessage.ALREADY_EXIST_INGREDIENT_UNIT
            ),
        )


class Base64ImageField(serializers.ImageField):
    """Поле сериализатора для преобразования Base64 в картинку"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeBaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор рецептов с минимальным набором полей для отображения в
    подписках, избранном и списке покупок
    """
    image = Base64ImageField()
    cooking_time = serializers.IntegerField(
        min_value=MIN_VALUE_COOKING_TIME, max_value=MAX_VALUE_COOKING_TIME
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_field = ('id', 'name', 'image', 'cooking_time',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для связей рецептов-ингредиентов при отображении рецепта"""
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(RecipeBaseSerializer):
    """Сериализатор для отображения рецептов"""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = IngredientRecipeSerializer(
        many=True, source='ingredientrecipe'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name'),
                message=ErrorMessage.ALREADY_EXIST_RECIPE_AUTHOR
            ),
        )

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Favorite.objects.filter(
            user=user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(
            user=user, recipe=obj
        ).exists()


class IngredientRecipeBaseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки связей рецептов с ингредиентами при создании и
    изменении рецепта
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(
        min_value=MIN_VALUE_AMOUNT, max_value=MAX_VALUE_AMOUNT
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount',)


class RecipeCreateUpdateSerializer(RecipeSerializer):
    """Сериализатор для создания и изменения рецептов"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    author = CustomUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientRecipeBaseSerializer(
        many=True, source='ingredientrecipe'
    )

    @transaction.atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredientrecipe')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                ingredient=ingredient['id'],
                recipe=recipe, amount=ingredient['amount']
            )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredientrecipe', {})
        super().update(instance, validated_data)
        if tags:
            instance.tags.clear()
            instance.tags.set(tags)
        if ingredients:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            for ingredient in ingredients:
                IngredientRecipe.objects.create(
                    ingredient=ingredient['id'],
                    recipe=instance, amount=ingredient['amount']
                )
        return instance

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                ErrorMessage.NOT_ADDED_TAG
            )
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                ErrorMessage.DOUBLE_TAGS
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                ErrorMessage.NOT_ADDED_INGREDIENT
            )
        return value

    def validate(self, data):
        ingredients = data['ingredientrecipe']
        ingredient_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_list) != len(set(ingredient_list)):
            raise serializers.ValidationError(
                ErrorMessage.DOUBLE_INGREDIENTS
            )
        return data

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class UserWithRecipeSerializer(CustomUserSerializer):
    """Сериализатор для отображения пользователей с подписками в Подписках"""
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes_limit = self.context['request'].GET.get('recipes_limit')
        instance = obj.recipes.all()
        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
            except ValueError:
                raise serializers.ValidationError(
                    ErrorMessage.RECIPES_LIMIT_TYPE
                )
            if recipes_limit < 0:
                raise serializers.ValidationError(
                    ErrorMessage.RECIPES_LIMIT_NOT_POSITIVE
                )
            instance = instance[:recipes_limit]
        return RecipeBaseSerializer(instance, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для Избранных рецептов"""
    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe',),
                message=ErrorMessage.ALREADY_EXIST_RECIPE_IN_FAVORITES
            ),
        )

    def to_representation(self, instance):
        instance = instance.recipe
        return RecipeBaseSerializer(instance, context=self.context).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для Списка покупок"""
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe',)
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message=ErrorMessage.ALREADY_EXIST_RECIPE_IN_SHOPPING_CART
            ),
        )

    def to_representation(self, instance):
        instance = instance.recipe
        return RecipeBaseSerializer(instance, context=self.context).data


class SubscribtionSerializer(serializers.ModelSerializer):
    """Сериализатор для Подписок"""
    class Meta:
        model = Subscription
        fields = ('user', 'author',)
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author',),
                message=ErrorMessage.ALREADY_EXIST_SUBSCRIBTION
            ),
        )

    def validate_author(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                ErrorMessage.SELF_SUBSCRIBTION_FORBIDDEN
            )
        return value

    def to_representation(self, instance):
        instance = instance.author
        return UserWithRecipeSerializer(instance, context=self.context).data
