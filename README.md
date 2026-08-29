# Cafe Django Project

Веб-приложение для управления столами и бронированием в кафе. Проект включает серверную часть на Django, REST API, админ-панель и фоновые задачи для уведомлений по email.

## Возможности

- **Столы** — просмотр списка столов с фото, описанием, количеством мест и характеристиками; поиск и фильтрация; отображение занятости в рабочие часы (8:00–18:00).
- **Избранное** — авторизованные пользователи могут добавлять столы в избранное.
- **Бронирование** — бронирование стола на выбранную дату и временной интервал через веб-интерфейс или API.
- **Аутентификация** — регистрация, вход, выход, сброс пароля по email.
- **REST API** — CRUD для бронирований и пользователей; аутентификация через Token, JWT и сессии (Djoser).
- **Документация API** — Swagger UI и ReDoc (drf-spectacular).
- **Админ-панель** — Django Admin с темой [Unfold](https://github.com/unfoldadmin/django-unfold).
- **Фоновые задачи** — Celery отправляет email всем пользователям при добавлении нового стола.
- **Логирование** — middleware записывает активность пользователей в `django-project/project/Log/usersActivity.log`.

## Стек технологий

| Компонент | Технология |
|-----------|------------|
| Backend | Django 6, Django REST Framework |
| База данных | PostgreSQL |
| Очередь задач | Celery + Redis |
| Аутентификация API | Djoser, SimpleJWT, Token Auth |
| Документация API | drf-spectacular |
| Админка | django-unfold |
| Зависимости | [uv](https://docs.astral.sh/uv/) / `pyproject.toml` |

## Структура проекта

```
cafe_django_project/
├── django-project/           # Django-приложение
│   ├── authentication/       # Пользователи, регистрация, сброс пароля, API
│   ├── table/                # Столы, характеристики, избранное
│   ├── reservation/          # Бронирования (веб + API)
│   ├── project/              # Настройки, URL, Celery, middleware
│   ├── templates/            # HTML-шаблоны
│   ├── media/                # Загруженные изображения столов
│   ├── settings.env          # Переменные окружения (не в git)
│   └── manage.py
├── scripts/
│   └── add_fake_data.py      # Генерация тестовых данных (Faker)
├── pyproject.toml
└── uv.lock
```

## Требования

- Python 3.13+
- PostgreSQL
- Redis (для Celery)
- [uv](https://docs.astral.sh/uv/) (рекомендуется) или pip

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <url-репозитория>
cd cafe_django_project
```

### 2. Установка зависимостей

```bash
uv sync
```

Или с pip:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate  # Linux / macOS
pip install -e .
```

### 3. База данных PostgreSQL

Создайте базу данных и пользователя (параметры по умолчанию из `settings.py`):

```sql
CREATE DATABASE django_cafe;
CREATE USER django WITH PASSWORD 'root';
GRANT ALL PRIVILEGES ON DATABASE django_cafe TO django;
```

При необходимости измените настройки подключения в `django-project/project/settings.py`.

### 4. Переменные окружения

Создайте файл `django-project/settings.env`:

```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
```

Переменные `EMAIL_HOST_*` нужны для сброса пароля и рассылки уведомлений о новых столах.

### 5. Миграции и суперпользователь

```bash
cd django-project
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

### 6. Запуск сервера разработки

```bash
uv run python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

### 7. Запуск Celery (опционально)

Убедитесь, что Redis запущен, затем в отдельном терминале:

```bash
cd django-project
uv run celery -A project worker -l info
```

## Основные URL

### Веб-интерфейс

| URL | Описание |
|-----|----------|
| `/` | Главная страница |
| `/tables/` | Список столов |
| `/tables/favorites` | Избранные столы |
| `/reservation/book_a_table/<id>` | Бронирование стола |
| `/reservation/list_booked_tables` | Мои бронирования |
| `/auth/login` | Вход |
| `/auth/register` | Регистрация |
| `/auth/password-reset-request` | Запрос сброса пароля |
| `/admin/` | Админ-панель |

### REST API

| URL | Описание |
|-----|----------|
| `/api/reservations/` | Список и создание бронирований |
| `/api/reservations/<id>/` | Детали, изменение, удаление бронирования |
| `/api/reservations/my/` | Бронирования текущего пользователя |
| `/api/users/` | Список и создание пользователей |
| `/api/auth/` | Эндпоинты Djoser (регистрация, JWT и т.д.) |
| `/api/schema/swagger-ui/` | Swagger UI |
| `/api/schema/redoc/` | ReDoc |

### Фильтрация бронирований (API)

Доступные query-параметры:

- `table__number` — номер стола
- `date` — дата бронирования (формат `YYYY-MM-DD`)

Пример: `/api/reservations/?table__number=5&date=2026-08-29`

## Тестовые данные

Скрипт для генерации данных с помощью Faker:

```bash
cd django-project
uv run python ../scripts/add_fake_data.py
```

Перед запуском убедитесь, что в базе есть пользователи и столы (или раскомментируйте соответствующие блоки в скрипте).

## Тесты

```bash
cd django-project
uv run python manage.py test
```

Тесты расположены в:

- `authentication/tests/`
- `reservation/tests/`
- `table/tests.py`

## Модели данных

- **User** — расширенная модель пользователя Django с поддержкой избранных столов.
- **Table** — стол (номер, фото, количество мест, описание, характеристики).
- **Feature** — характеристика стола (например, «у окна», «кондиционер»).
- **Favorites** — связь пользователя и избранного стола.
- **Reservation** — бронирование (стол, пользователь, дата, час начала и окончания).
- **PasswordResetToken** — токен для сброса пароля.

## Лицензия

Уточните лицензию при публикации проекта.
