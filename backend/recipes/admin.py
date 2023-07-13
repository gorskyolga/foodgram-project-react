from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Subscription,
    Tag, TagRecipe
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('measurement_unit',)
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'pub_date', 'author', 'email', 'name', 'added_to_favorites',
    )
    list_filter = ('tags',)
    list_editable = ('author', 'name',)
    search_fields = ('name', 'author__username', 'author__email',)
    inlines = (IngredientRecipeInline, TagRecipeInline,)

    def added_to_favorites(self, obj) -> int:
        return obj.favorites.count()

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'favorites', 'author', 'ingredientrecipe', 'tagrecipe_set'
        )
        return queryset

    def email(self, obj) -> str:
        return obj.author.email


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'username', 'email', 'tag',)
    list_filter = ('recipe__tags',)
    list_editable = ('tag',)
    search_fields = (
        'recipe__name', 'recipe__author__username', 'recipe__author__email',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('recipe')
        return queryset

    def email(self, obj) -> str:
        return obj.recipe.author.email

    @admin.display(description='Автор рецепта')
    def username(self, obj) -> str:
        return obj.recipe.author.username


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'recipe', 'ingredient', 'amount', 'username', 'email',
    )
    list_filter = ('recipe__tags',)
    list_editable = ('ingredient', 'amount',)
    search_fields = (
        'recipe__name', 'recipe__author__username', 'recipe__author__email',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('recipe')
        return queryset

    def email(self, obj) -> str:
        return obj.recipe.author.email

    @admin.display(description='Автор рецепта')
    def username(self, obj) -> str:
        return obj.recipe.author.username


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'email', 'recipe',)
    list_filter = ('recipe__tags',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user__username', 'user__email', 'recipe__name',)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('user', 'recipe')
        return queryset

    def email(self, obj) -> str:
        return obj.user.email


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'user_email', 'author', 'author_email',)
    list_filter = ('user', 'author',)
    list_editable = ('user', 'author',)
    search_fields = (
        'user__username', 'user__email', 'author__username', 'author__email',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('user', 'author')
        return queryset

    @admin.display(description='Email автора')
    def author_email(self, obj) -> str:
        return obj.author.email

    @admin.display(description='Email подписчика')
    def user_email(self, obj) -> str:
        return obj.user.email


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'email', 'recipe',)
    list_filter = ('recipe__tags',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user__username', 'user__email', 'recipe__name',)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('user', 'recipe')
        return queryset

    def email(self, obj) -> str:
        return obj.user.email
