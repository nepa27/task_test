from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import User, Session, Role, BusinessElement, AccessRule
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, RoleSerializer,
    BusinessElementSerializer, AccessRuleSerializer
)
from .permissions import CanManageAccessRules


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet для аутентификации и управления профилем пользователя.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Регистрирует нового пользователя.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Пользователь успешно зарегистрирован'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Аутентифицирует пользователя и создает сессию.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(
                    email=serializer.validated_data['email'], is_active=True
                )
                if user.check_password(serializer.validated_data['password']):
                    token = user.generate_token()
                    Session.objects.create(
                        user=user,
                        token=token,
                        expires_at=timezone.now() + timedelta(days=7)
                    )
                    return Response(
                        {'token': token}, status=status.HTTP_200_OK
                    )
            except User.DoesNotExist:
                pass
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Завершает сессию пользователя.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            Session.objects.filter(token=token).delete()
        return Response({'message': 'Успешный выход'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Обновляет профиль пользователя.
        """
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        """
        Деактивирует аккаунт пользователя и удаляет его сессии.
        """
        request.user.is_active = False
        request.user.save()
        Session.objects.filter(user=request.user).delete()
        return Response({'message': 'Аккаунт удален'}, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления ролями пользователей.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated, CanManageAccessRules)


class BusinessElementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления бизнес-элементами.
    """
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    permission_classes = (IsAuthenticated, CanManageAccessRules)


class AccessRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления правилами доступа.
    """
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    permission_classes = (IsAuthenticated, CanManageAccessRules)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mock_users_view(request):
    """
    Мок-эндпоинт для списка пользователей.
    """
    return Response({'data': 'Список пользователей'})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mock_products_view(request):
    """
    Мок-эндпоинт для списка и создания товаров.
    """
    if request.method == 'GET':
        return Response({'data': 'Список товаров'})
    return Response({'data': 'Товар создан'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def mock_orders_view(request):
    """
    Мок-эндпоинт для заказов (просмотр, обновление, удаление).
    """
    if request.method == 'GET':
        return Response({'data': 'Список заказов'})
    elif request.method == 'PUT':
        return Response({'data': 'Заказ обновлен'})
    return Response({'data': 'Заказ удален'})
