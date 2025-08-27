from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role, BusinessElement, AccessRule


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'auth_core':
        admin_role, created = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Администратор системы'}
        )
        user_role, created = Role.objects.get_or_create(
            name='user',
            defaults={'description': 'Обычный пользователь'}
        )

        users_element, created = BusinessElement.objects.get_or_create(
            name='users',
            defaults={'description': 'Управление пользователями'}
        )
        products_element, created = BusinessElement.objects.get_or_create(
            name='products',
            defaults={'description': 'Управление товарами'}
        )
        orders_element, created = BusinessElement.objects.get_or_create(
            name='orders',
            defaults={'description': 'Управление заказами'}
        )
        access_rules_element, created = BusinessElement.objects.get_or_create(
            name='access_rules',
            defaults={'description': 'Управление правами доступа'}
        )

        AccessRule.objects.get_or_create(
            role=admin_role,
            element=users_element,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True
            }
        )

        AccessRule.objects.get_or_create(
            role=admin_role,
            element=access_rules_element,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True
            }
        )
