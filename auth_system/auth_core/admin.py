from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, BusinessElement, AccessRule, Session


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная админка для модели пользователя.
    """
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'patronymic', 'role')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups',
                'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2'
            ),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Админка для модели роли.
    """
    list_display = ('name', 'description')


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    """
    Админка для модели бизнес-элемента.
    """
    list_display = ('name', 'description')


@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    """
    Админка для модели правила доступа.
    """
    list_display = (
        'role', 'element', 'read_permission', 'create_permission'
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """
    Админка для модели сессии пользователя.
    """
    list_display = ('user', 'created_at', 'expires_at')
