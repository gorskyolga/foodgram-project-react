from django_filters.rest_framework import DjangoFilterBackend

from django.db import transaction
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.constants import (
    SHOPPING_LIST_FILE_CONTENT_TYPE, SHOPPING_LIST_FILE_NAME, HTTPMethod
)
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAuthorChangeRecipePermission
from api.serializers import (
    FavoriteSerializer, IngredientSerializer, RecipeCreateUpdateSerializer,
    RecipeSerializer, ShoppingCartSerializer, SubscribtionSerializer,
    TagSerializer
)
from recipes.models import (
    Ingredient, IngredientRecipe, Favorite, Recipe, ShoppingCart, Subscription,
    Tag
)

User = get_user_model()


class CreateDestroyViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """Базовый класс вьюсета для создания и удаления объекта"""
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для отображения, создания, изменения и удаления рецептов и
    формирования текстового файла со Списком покупок
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (
        IsAuthorChangeRecipePermission, permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    @action(methods=(HTTPMethod.get,), detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by('ingredient__name').annotate(total_amount=Sum('amount'))
        content = 'Список покупок:'
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_name = ingredient['ingredient__name']
            ingredient_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['total_amount']
            ingredient_list.append(
                f'- {ingredient_name} ({ingredient_unit}) - {amount}'
            )
        if ingredient_list:
            content += '\n' + '\n'.join(ingredient_list)
        else:
            content += '\nВ Списке покупок отсутствуют рецепты.'
        response = HttpResponse(
            content, content_type=SHOPPING_LIST_FILE_CONTENT_TYPE
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{SHOPPING_LIST_FILE_NAME}"'
        )
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter


class FavoriteViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления, удаления рецептов в Избранное"""
    serializer_class = FavoriteSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return super().get_serializer(*args, **kwargs)
        data = {
            'user': self.request.user.id,
            'recipe': self.kwargs.get('recipe_id')
        }
        return FavoriteSerializer(data=data, context={'request': self.request})

    def get_queryset(self):
        return self.request.user.favorites.all()

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        instance = get_object_or_404(
            Favorite, user=request.user, recipe=recipe
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(CreateDestroyViewSet):
    """Вьюсет для добавления и удаления рецептов из Списка покупок"""
    serializer_class = ShoppingCartSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return super().get_serializer(*args, **kwargs)
        data = {
            'user': self.request.user.id,
            'recipe': self.kwargs.get('recipe_id')
        }
        return ShoppingCartSerializer(
            data=data, context={'request': self.request}
        )

    def get_queryset(self):
        return self.request.user.shopping_cart.all()

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
        instance = get_object_or_404(
            ShoppingCart, user=request.user, recipe=recipe
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribtionViewSet(CreateDestroyViewSet, mixins.ListModelMixin):
    """Вьюсет для добавления, удаления авторов в Подписки"""
    serializer_class = SubscribtionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return super().get_serializer(*args, **kwargs)
        data = {
            'user': self.request.user.id,
            'author': self.kwargs.get('author_id')
        }
        return SubscribtionSerializer(
            data=data, context={'request': self.request}
        )

    def get_queryset(self):
        return self.request.user.subscriptions.all()

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('author_id'))
        instance = get_object_or_404(
            Subscription, user=request.user, author=author
        )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
