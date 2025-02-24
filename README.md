# Referral System API

## Описание
Этот проект представляет собой RESTful API для реферальной системы.
Позволяет пользователям регистрироваться, управлять реферальными кодами и отслеживать своих рефералов.

## Функциональность
- Регистрация и аутентификация пользователей
- Создание и удаление реферального кода
- Указание срока годности реферального кода
- Получение реферального кода по email реферера
- Регистрация по реферальному коду
- Получение информации о рефералах по ID реферера
- UI-документация API (Swagger)


## Технологический стек
- **Язык**: Python3.12
- **Веб-фреймворк**: FastAPI
- **База данных**: PostgreSQL
- **Миграции**: Alembic

## Установка и запуск проекта
### 1. Клонирование репозитория
```sh
    git clone <repo-url>
    cd <repo-folder>
```

### 2. Создание виртуального окружения и установка зависимостей
```sh
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` на основе `.env.example` в корне проекта и заполните его.


### 4. Поднятие инфраструктуры в Docker
```sh
    docker-compose up -d
```

### 5. Запуск BASH скриптов для инициализации и запуска сервисов
```sh
    ./scripts/start.sh
```

## Документация API
После запуска проекта, документация доступна по адресу:
- Swagger UI: `http://localhost:8000/docs`
