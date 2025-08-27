# Система аутентификации и авторизации
## Простая система управления доступом на Django и DRF с гибридной моделью (RBAC + ABAC).

### Основные компоненты
Пользователь (User) - имеет роль и стандартные поля профиля
Роль (Role) - группа пользователей (admin, user)
Бизнес-элемент (BusinessElement) - защищаемый ресурс (users, products, orders, access_rules)
Правило доступа (AccessRule) - определяет какие CRUD-операции разрешены роли над элементом

### Права по умолчанию
Админ (admin) имеет полные права на:

Управление пользователями (users)
Управление правами доступа (access_rules)
Обычный пользователь (user) не имеет прав по умолчанию

### Аутентификация
JWT-токен в заголовке запроса:
```
Authorization: Bearer <ваш_токен>
Сессии хранятся 7 дней и автоматически обновляются.
```

## Запуск проекта
### Локальное развертывание
Установите Python и pip (команды для Ubuntu).
```
sudo apt-get install python
sudo apt-get install pip
```
Создайте виртуальное окружение
```
python -m venv venv
source venv/bin/activate    # (Ubuntu)
./venv/Scripts/python       # (Windows)
```
Затем установите необходимые зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
Запустите проект:

```
cd auth_system
python manage.py runserver
```
Если вы все правильно сделали, то высветится приглашение
```
System check identified no issues (0 silenced).
August 27, 2025 - 21:44:20
Django version 5.2.1, using settings 'auth_system.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/

# API Endpoints

## 🔐 Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/api/auth/register/` | Регистрация пользователя |
| `POST` | `/api/auth/login/` | Вход в систему |
| `POST` | `/api/auth/logout/` | Выход из системы |
| `PUT` | `/api/auth/update_profile/` | Обновление профиля |
| `DELETE` | `/api/auth/delete_account/` | Удаление аккаунта |

## ⚙️ Управление доступом (только для админов)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET`, `POST`, `PUT`, `DELETE` | `/api/roles/` | CRUD операции для ролей |
| `GET`, `POST`, `PUT`, `DELETE` | `/api/elements/` | CRUD операции для бизнес-элементов |
| `GET`, `POST`, `PUT`, `DELETE` | `/api/rules/` | CRUD операции для правил доступа |

## 🧪 Тестовые endpoints

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/mock/users/` | Получить список пользователей |
| `GET`, `POST` | `/api/mock/products/` | Работа с товарами |
| `GET`, `PUT`, `DELETE` | `/api/mock/orders/` | Работа с заказами |

## Автор
+ [Александр Непочатых](https://github.com/nepa27)