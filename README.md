# Барбершоп "Горшок"

Веб-приложение для управления барбершопом на Django.  
Клиенты могут просматривать услуги, записываться и оставлять отзывы.  
Мастера и администраторы управляют расписанием, профилями и модерируют отзывы с помощью Mistral AI.

---

## Структура проекта

```
May_25/
├── barbershop/           # Конфигурация Django-проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Основное приложение
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── mistral.py        # Интеграция с Mistral AI
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── templates/            # Шаблоны Django
│   └── ...
├── static/               # Статические файлы
│   └── ...
├── manage.py
├── requirements.txt
├── .env                  # Переменные окружения
└── README.md
```

---

## Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Greg-Miles/May_25.git
cd May_25
```

### 2. Установите зависимости

**С помощью Poetry (рекомендуется):**
```bash
poetry install
poetry shell
```

**Или через venv + pip:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Настройте переменные окружения

Создайте файл `.env` в корне проекта:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
MISTRAL_MODERATION_KEY=your_mistral_key
```

### 4. Примените миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Запустите сервер

```bash
python manage.py runserver
```
- Откройте http://127.0.0.1:8000/

### 6. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

---

## Особенности

- Модуль `core/mistral.py` использует ключ `MISTRAL_MODERATION_KEY` для проверки отзывов через Mistral AI.
- После сохранения отзыва сигнал в `core/signals.py` вызывает модерацию и обновляет статус.
- Непрошедшие модерацию отзывы не публикуются.

---

## Тестирование и линтинг

```bash
python manage.py test
flake8
```

---

## Лицензия

Учебный проект. Используйте для обучения и личных целей.