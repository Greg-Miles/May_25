# Барбершоп "Горшок"

## Описание проекта

Веб-приложение для барбершопа "Горшок" на Django.  
Клиенты могут просматривать услуги, записываться, оставлять отзывы.  
Мастера и админы — управлять записями, профилями и модерацией отзывов через Mistral AI.

## Структура проекта

├ manage.py  
├ .env                 ← ваш файл с переменными окружения  
├ requirements.txt  
├ barbershop/          ← Django-пакет  
│  ├ settings.py       ← настройки проекта  
│  ├ urls.py  
│  └ …  
└ core/                ← основное приложение  
   ├ models.py  
   ├ views.py  
   ├ forms.py  
   ├ signals.py  
   ├ mistral.py        ← модуль работы с Mistral AI  
   └ …  

## Требования

• Python 3.8+  
• Django 4.0+  
• Poetry 1.0+ (рекомендуется) или pip + venv  
• PostgreSQL 12+ (опционально)  

## Установка

### Клонирование
```bash
git clone https://github.com/Greg-Miles/May_25.git
cd May_25
```

### Создать и активировать виртуальное окружение

С Poetry (рекомендуется):
```bash
poetry install
poetry shell
```

С venv + pip:
```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Настроить файл `.env`

В корне проекта (рядом с `manage.py`) создайте файл `.env` (UTF-8 без BOM).  
Пример содержимого:

```env:.env
# Django
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost




# Дополнительные переменные, если нужно
# EMAIL_HOST=...
# EMAIL_PORT=...
```

### Загрузка `.env` в `settings.py`

В `barbershop/settings.py` добавьте в начало:
```python:barbershop/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# загружаем .env
load_dotenv(dotenv_path=BASE_DIR / '.env')

# далее — все стандартные настройки Django
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
...
```

## Установка и миграции БД

По умолчанию используется SQLite:
```bash
python manage.py makemigrations
python manage.py migrate
```

Если PostgreSQL — настройте `DATABASES` в `settings.py` или используйте переменную `DATABASE_URL`, например через `dj-database-url`.

## Запуск проекта

```bash
python manage.py runserver
```
Открыть в браузере: http://127.0.0.1:8000/

Админ-панель: http://127.0.0.1:8000/admin/  
Создать суперпользователя:
```bash
python manage.py createsuperuser
```

## Особенности

— В `core/mistral.py` модуль `is_good_review()` берёт ключ MISTRAL_MODERATION_KEY из окружения и передаёт его в Mistral AI.  
— Сигнал `core/signals.py` после сохранения отзыва вызывает `is_good_review()` и обновляет поле `ai_checked_status`.  
— Если отзыв не прошёл модерацию — он не публикуется и помечается `ai_cancelled`.  

## Настройка Jazzmin (опционально)

Если вы используете Jazzmin для админ-темы, можно добавить в `settings.py`:

```python:barbershop/settings.py
JAZZMIN_SETTINGS = {
    "site_url": "/",
    "topmenu_links": [
        {"name": "На сайт", "url": "/", "icon": "fas fa-home"},
    ],
    "usermenu_links": [
        {"name": "Exit to site", "url": "/", "icon": "fas fa-external-link-alt", "new_window": False},
    ],
}
```

## Тестирование и линтинг

```bash
python manage.py test
flake8
```

## Лицензия

Проект является учебным и не распространяется, но если вы хотите его скачать, то чтож я вам сделаю.