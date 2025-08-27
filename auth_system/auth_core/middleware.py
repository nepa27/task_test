from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import Session
from django.utils import timezone


class CustomAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware для аутентификации пользователя по JWT-токену из заголовка.
    Если токен валиден, устанавливает request.user как пользователя из сессии.
    """
    def process_request(self, request):
        """
        Обрабатывает входящий запрос, устанавливает пользователя в request.user.
        Если токен не найден или невалиден, устанавливает AnonymousUser.
        """
        if not hasattr(request, 'user') or request.user.is_anonymous:
            request.user = AnonymousUser()

        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                session = Session.objects.select_related('user').get(token=token)
                if session.is_valid():
                    request.user = session.user
                    session.refresh()
                    session.user.last_login = timezone.now()
                    session.user.save(update_fields=['last_login'])
            except Session.DoesNotExist:
                pass
