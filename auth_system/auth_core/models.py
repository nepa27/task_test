from datetime import datetime, timedelta

import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
import jwt


class Role(models.Model):
    """
    Модель роли пользователя.
    name: Название роли.
    description: Описание роли.
    """
    name = models.CharField(
        max_length=50, unique=True, verbose_name="Название"
    )
    description = models.TextField(
        blank=True, verbose_name="Описание"
    )

    def __str__(self):
        """Строковое представление роли."""
        return self.name


class BusinessElement(models.Model):
    """
    Модель бизнес-элемента.
    name: Название элемента.
    description: Описание элемента.
    """
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название"
    )
    description = models.TextField(
        blank=True, verbose_name="Описание"
    )

    def __str__(self):
        """Строковое представление бизнес-элемента."""
        return self.name


class AccessRule(models.Model):
    """
    Модель правила доступа для роли к бизнес-элементу.
    """
    role = models.ForeignKey(
        Role, on_delete=models.CASCADE, verbose_name="Роль"
    )
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE, verbose_name="Бизнес-элемент"
    )
    read_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на чтение"
    )
    read_all_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на чтение всех"
    )
    create_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на создание"
    )
    update_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на изменение"
    )
    update_all_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на изменение всех"
    )
    delete_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на удаление"
    )
    delete_all_permission = models.BooleanField(
        default=False, verbose_name="Разрешение на удаление всех"
    )

    class Meta:
        unique_together = ('role', 'element')


class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает обычного пользователя.
        """
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя.
    """
    first_name = models.CharField(
        max_length=50, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=50, verbose_name="Фамилия"
    )
    patronymic = models.CharField(
        max_length=50, blank=True, verbose_name="Отчество"
    )
    email = models.EmailField(
        unique=True, verbose_name="Email"
    )
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Роль"
    )
    is_staff = models.BooleanField(
        default=False, verbose_name="Персонал"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Активен"
    )
    is_superuser = models.BooleanField(
        default=False, verbose_name="Суперпользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def set_password(self, raw_password):
        """
        Устанавливает пароль пользователя, используя bcrypt.
        """
        hashed_password = bcrypt.hashpw(
            raw_password.encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')
        self.password = hashed_password

    def check_password(self, raw_password):
        """
        Проверяет пароль пользователя.
        """
        try:
            return bcrypt.checkpw(
                raw_password.encode('utf-8'), self.password.encode('utf-8')
            )
        except (ValueError, AttributeError):
            return False

    def generate_token(self):
        """
        Генерирует JWT токен для пользователя.
        """
        payload = {
            'user_id': self.id,
            'exp': datetime.now() + timedelta(days=7),
            'iat': datetime.now()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def verify_token(token):
        """
        Проверяет валидность JWT токена пользователя.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256']
            )
            return User.objects.get(id=payload['user_id'], is_active=True)
        except (
            jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist
        ):
            return None

    def __str__(self):
        """Строковое представление пользователя."""
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def is_anonymous(self):
        """Пользователь не является анонимным."""
        return False

    @property
    def is_authenticated(self):
        """Пользователь всегда аутентифицирован."""
        return True


class Session(models.Model):
    """
    Модель сессии пользователя.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    token = models.CharField(
        max_length=500, unique=True, verbose_name="Токен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    expires_at = models.DateTimeField(
        verbose_name="Дата истечения"
    )

    def is_valid(self):
        """
        Проверяет, действительна ли сессия.
        """
        return self.expires_at > timezone.now() and self.user.is_active

    def refresh(self):
        """
        Обновляет срок действия сессии.
        """
        self.expires_at = timezone.now() + timedelta(days=7)
        self.save()
