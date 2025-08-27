from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, RoleViewSet, BusinessElementViewSet, AccessRuleViewSet
from .views import mock_users_view, mock_products_view, mock_orders_view

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'roles', RoleViewSet)
router.register(r'elements', BusinessElementViewSet)
router.register(r'rules', AccessRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('mock/users/', mock_users_view),
    path('mock/products/', mock_products_view),
    path('mock/orders/', mock_orders_view),
]