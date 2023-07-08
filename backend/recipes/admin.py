from django.contrib import admin

from recipes.models import (
    Favorite, Ingredient, IngredientRecipe, Recipe, ShoppingCart, Subscription,
    Tag, TagRecipe
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug',)
    list_filter = ('name', 'slug',)
    list_editable = ('name', 'color', 'slug',)
    search_fields = ('name', 'slug',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit',)
    list_filter = ('name',)
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
        'id', 'pub_date', 'author', 'name', 'cooking_time',
        'added_to_favorites',
    )
    list_filter = ('author', 'name', 'tags',)
    list_editable = ('author', 'name', 'cooking_time',)
    search_fields = ('author', 'name', 'tags',)
    inlines = (IngredientRecipeInline, TagRecipeInline,)

    def added_to_favorites(self, obj) -> int:
        return obj.favorites.count()


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag',)
    list_filter = ('recipe', 'tag',)
    list_editable = ('tag',)
    search_fields = ('recipe', 'tag',)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount',)
    list_filter = ('recipe', 'ingredient',)
    list_editable = ('ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author',)
    list_filter = ('user', 'author',)
    list_editable = ('user', 'author',)
    search_fields = ('user', 'author',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe',)
    list_filter = ('user', 'recipe',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
