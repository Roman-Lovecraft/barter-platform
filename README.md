## Описание
Barter Platform — это веб-приложение для размещения объявлений и обмена товарами между пользователями.

## Технологический стек

- **Язык**: Python 3.8+
- **Веб-фреймворк**: Django 4+ (с использованием встроенной ORM)
- **Шаблонизация**: Django Templates для создания HTML-страниц
- **База данных**: SQLite (по умолчанию) или PostgreSQL (опционально)
- **Тестирование**: Unittest (встроенная система тестирования Django)
- **Документация**: README.md с инструкциями по установке, настройке и запуску проекта

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/your-repo/barter-platform.git
   cd barter-platform
   ```

2. Установите виртуальное окружение и зависимости:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Выполните миграции базы данных:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Создайте суперпользователя:
   ```
   python manage.py createsuperuser
   ```

5. Запустите сервер разработки:
   ```
   python manage.py runserver
   ```

6. Откройте приложение в браузере:
   ```
   http://127.0.0.1:8000/
   ```
   Доступ к админ панелю
   http://127.0.0.1:8000/admin/

Запуск тестов
Для запуска тестов выполните:
   ```
   python manage.py test
   ```
Лицензия
Этот проект лицензирован под MIT License.

