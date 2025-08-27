from rest_framework import serializers
from .models import User, Role, BusinessElement, AccessRule


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'patronymic', 'email',
            'password', 'password_confirm'
        )

    def validate(self, data):
        """
        Проверяет совпадение паролей.
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        """
        Создает нового пользователя.
        """
        validated_data.pop('password_confirm')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    """
    email = serializers.EmailField()
    password = serializers.CharField()


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class RoleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели роли.
    """
    class Meta:
        model = Role
        fields = '__all__'


class BusinessElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели бизнес-элемента.
    """
    class Meta:
        model = BusinessElement
        fields = '__all__'


class AccessRuleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели правила доступа.
    """
    class Meta:
        model = AccessRule
        fields = '__all__'
