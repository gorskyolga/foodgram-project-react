from rest_framework import permissions

from api.constants import ErrorMessage


class IsAuthorChangeRecipePermission(permissions.BasePermission):
    """Permission для изменения и удаления рецептов."""

    message = ErrorMessage.IS_NOT_RECIPE_OWNER

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
