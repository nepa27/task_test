from rest_framework import permissions
from .models import BusinessElement, AccessRule


class HasPermission(permissions.BasePermission):
    """
    Базовый класс разрешения для проверки доступа к бизнес-элементу.
    """

    def __init__(self, element_name, permission_type, check_ownership=False):
        """
        Инициализация разрешения.
        :param element_name: Название бизнес-элемента
        :param permission_type: Тип разрешения (например, 'read_permission')
        :param check_ownership: Проверять ли владение объектом
        """
        self.element_name = element_name
        self.permission_type = permission_type
        self.check_ownership = check_ownership

    def has_permission(self, request, view):
        """
        Проверяет разрешение на уровне запроса.
        """
        if not request.user or not request.user.is_active:
            return False

        if self.permission_type == 'create_permission':
            self.check_ownership = False

        try:
            element = BusinessElement.objects.get(name=self.element_name)
            access_rule = AccessRule.objects.get(
                role=request.user.role, element=element
            )
            return getattr(access_rule, self.permission_type, False)
        except (BusinessElement.DoesNotExist, AccessRule.DoesNotExist):
            return False

    def has_object_permission(self, request, view, obj):
        """
        Проверяет разрешение на уровне объекта.
        """
        if not self.has_permission(request, view):
            return False

        # Если проверяем владение и у объекта есть владелец
        if self.check_ownership and hasattr(obj, 'owner'):
            # Для всех прав проверяем, является ли пользователь владельцем
            if self.permission_type in [
                'read_all_permission', 'update_all_permission',
                'delete_all_permission'
            ]:
                return True
            return obj.owner == request.user

        return True


class CanReadUsers(HasPermission):
    """
    Разрешение на чтение пользователей.
    """

    def __init__(self):
        super().__init__('users', 'read_permission')


class CanManageAccessRules(HasPermission):
    """
    Разрешение на управление правилами доступа.
    """

    def __init__(self):
        super().__init__('access_rules', 'update_permission')
