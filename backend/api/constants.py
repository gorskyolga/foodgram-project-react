REGEX_HEX_COLOR = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
REGEX_USERNAME = r'^[\w.@+-]+\Z'

MIN_VALUE_COOKING_TIME = 1
MAX_VALUE_COOKING_TIME = 10000
MIN_VALUE_AMOUNT = 1
MAX_VALUE_AMOUNT = 100000


class ErrorMessage:
    REGEX_HEX_COLOR = (
        f'Значение `color` не удовлетворяет шаблону "{REGEX_HEX_COLOR}"'
    )
    REGEX_USERNAME = (
        f'Значение `username` не удовлетворяет шаблону "{REGEX_USERNAME}"'
    )
    IS_NOT_RECIPE_OWNER = 'Изменение и удаление чужих рецептов запрещено'
    ALREADY_EXIST_INGREDIENT_UNIT = (
        'Такое сочетание имени ингредиента и единицы измерения уже существует'
    )
    ALREADY_EXIST_RECIPE_AUTHOR = (
        'Автор не может создать два рецепта с одинаковым названием'
    )
    RECIPES_LIMIT_TYPE = 'Значение "recipes_limit" должно быть числом!'
    ALREADY_EXIST_RECIPE_IN_SHOPPING_CART = (
        'Добавить рецепт в Список покупок дважды невозможно'
    )
    ALREADY_EXIST_RECIPE_IN_FAVORITES = (
        'Добавить дважды рецепт в избранное невозможно'
    )
    ALREADY_EXIST_SUBSCRIBTION = (
        'Подписаться дважды на одного пользователя невозможно'
    )
    SELF_SUBSCRIBTION_FORBIDDEN = 'Подписаться на самого себя невозможно'
    NOT_ADDED_TAG = 'Необходимо указать хотя бы один тег рецепта'
    DOUBLE_TAGS = 'Значения тегов не должны дублироваться'
    NOT_ADDED_INGREDIENT = 'Необходимо указать хотя бы один ингредиент рецепта'
    DOUBLE_INGREDIENTS = 'Ингредиенты в рецепте не должны дублироваться'
    NOT_EXISTED_RECIPE = 'Такого рецепта не существует'
    RECIPE_NOT_IN_SHOPPING_CART = (
        'Рецепт отсутствует в Списке покупок и не может быть удален из него'
    )
    RECIPE_NOT_IN_FAVORITES = (
        'Рецепт отсутствует в Избранном и не может быть удален из него'
    )
    AUTHOR_NOT_IN_SUBSCRIPTION = (
        'Автор отсутствует в Подписках и не может быть удален из них'
    )


class HTTPMethod:
    GET = 'GET'
    get = 'get'
    POST = 'POST'
    post = 'post'
    PUT = 'PUT'
    put = 'put'
    PATCH = 'PATCH'
    patch = 'patch'
    DELETE = 'DELETE'
    delete = 'delete'
