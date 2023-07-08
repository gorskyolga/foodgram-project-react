from django.urls import include, path
from rest_framework import routers

from api.views import (
    FavoriteViewSet, IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
    SubscribtionViewSet, TagViewSet
)


router = routers.DefaultRouter()
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shopping_cart_recipes'
)
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorites'
)
router.register(
    r'users/(?P<author_id>\d+)/subscribe', SubscribtionViewSet,
    basename='subscribe'
)
router.register(
    'users/subscriptions', SubscribtionViewSet, basename='subscribtions'
)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
