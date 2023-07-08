from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'pk', 'email', 'username', 'first_name', 'last_name', 'password',
    )
    list_filter = ('email', 'username',)
    list_editable = ('first_name', 'last_name', 'password',)
    search_fields = ('email', 'username',)


admin.site.unregister(Group)
