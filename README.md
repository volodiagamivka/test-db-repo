# Database Project

Flask проект з базою даних для управління користувачами, категоріями та властивостями.

**📖 Swagger документація доступна за адресою: `/api/docs/`**

## 🚀 Швидкий старт

### Локальний запуск

#### 1. Клонування репозиторію

```bash
git clone <URL_РЕПОЗИТОРІЮ>
cd test-db-repo
```

#### 2. Створення віртуального середовища

```bash
python3 -m venv venv
source venv/bin/activate  # На macOS/Linux
# або
venv\Scripts\activate     # На Windows
```

#### 3. Встановлення залежностей

```bash
pip install -r requirements.txt
```

#### 4. Налаштування змінних середовища

Створіть файл `.env` в корені проекту:

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=database_lab1_eer
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

#### 5. Запуск додатку

```bash
python app.py
```

Додаток буде доступний за адресою: `http://localhost:5000`

Swagger документація: `http://localhost:5000/api/docs/`

### 📦 Деплой на Azure

#### Варіант 1: Azure Virtual Machine (Рекомендовано) 🖥️

**📘 Детальна покрокова інструкція: [AZURE_VM_DEPLOYMENT.md](AZURE_VM_DEPLOYMENT.md)**

**🚀 Швидкий старт: [VM_QUICKSTART.md](VM_QUICKSTART.md)**

Основні кроки:

1. Створіть Azure MySQL Database
2. Створіть Ubuntu 22.04 VM
3. Підключіться по SSH
4. Встановіть Python, Nginx, залежності
5. Налаштуйте додаток вручну
6. Відкрийте Swagger: `http://your-vm-ip/api/docs/`

**Переваги VM:**

- ✅ Повний контроль над середовищем
- ✅ Можливість налаштування Nginx, SSL
- ✅ Легше налагоджувати проблеми
- ✅ Підходить для лабораторних робіт

#### Варіант 2: Azure Web App

**Детальна інструкція: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)**

Короткий огляд:

1. Створіть Azure MySQL Database
2. Створіть Azure Web App (Python 3.11)
3. Налаштуйте змінні середовища
4. Задеплойте код через GitHub Actions
5. Відкрийте Swagger: `https://your-app.azurewebsites.net/api/docs/`

**Переваги Web App:**

- ✅ Простіше в налаштуванні
- ✅ Автоматичне масштабування
- ✅ Вбудований CI/CD через GitHub Actions

## Структура проекту

```
database-main/
├── app.py                 # Головний файл додатку
├── database.py           # Конфігурація бази даних
├── config/
│   └── app.yml          # Конфігурація додатку
├── my_project/
│   ├── auth/
│   │   ├── controller/   # Контролери
│   │   ├── dao/         # Data Access Objects
│   │   ├── models/      # Моделі даних
│   │   ├── route/       # Маршрути API
│   │   └── service/     # Бізнес-логіка
│   └── db_init.py       # Ініціалізація бази даних
├── requirements.txt     # Залежності Python
└── README.md           # Цей файл
```

## 📚 API Endpoints

Всі endpoints доступні через Swagger UI за адресою `/api/docs/`

### Users (Користувачі)

- `GET /users` - Отримати всіх користувачів
- `GET /users/{user_id}` - Отримати користувача за ID
- `POST /users` - Створити нового користувача
- `PUT /users/{user_id}` - Оновити користувача
- `DELETE /users/{user_id}` - Видалити користувача
- `GET /users_with_properties` - Отримати користувачів з властивостями

### Categories (Категорії)

- `GET /categories` - Отримати всі категорії
- `GET /categories/{category_id}` - Отримати категорію за ID
- `POST /categories` - Створити нову категорію
- `PUT /categories/{category_id}` - Оновити категорію
- `DELETE /categories/{category_id}` - Видалити категорію

### Properties (Властивості)

- `GET /properties` - Отримати всі властивості
- `GET /properties/{property_id}` - Отримати властивість за ID
- `POST /properties` - Створити нову властивість
- `PUT /properties/{property_id}` - Оновити властивість
- `DELETE /properties/{property_id}` - Видалити властивість

### Property Categories (Зв'язки)

- `GET /property-categories` - Отримати всі зв'язки
- `GET /property-categories/{id}` - Отримати зв'язок за ID
- `POST /property-categories` - Створити новий зв'язок
- `PUT /property-categories/{id}` - Оновити зв'язок
- `DELETE /property-categories/{id}` - Видалити зв'язок

## 🛠 Технології

- **Flask** - Web фреймворк
- **SQLAlchemy** - ORM для роботи з базою даних
- **PyMySQL** - MySQL драйвер для Python
- **Flasgger** - Swagger/OpenAPI документація
- **Gunicorn** - WSGI HTTP сервер для production
- **python-dotenv** - Управління змінними середовища

## 🧪 Тестування API

### За допомогою Swagger UI

1. Відкрийте `/api/docs/` в браузері
2. Виберіть endpoint
3. Натисніть "Try it out"
4. Введіть параметри (якщо потрібно)
5. Натисніть "Execute"

### За допомогою curl

```bash
# Отримати всіх користувачів
curl http://localhost:5000/users

# Створити користувача
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Іван Петренко","email":"ivan@example.com"}'

# Отримати користувача за ID
curl http://localhost:5000/users/1

# Оновити користувача
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Нове Ім'я","email":"newemail@example.com"}'

# Видалити користувача
curl -X DELETE http://localhost:5000/users/1
```

### За допомогою Postman

1. Імпортуйте OpenAPI специфікацію з `/apispec.json`
2. Тестуйте endpoints через Postman

## 💻 Розробка

Для розробки рекомендується:

1. Використовувати віртуальне середовище
2. Дотримуватися структури проекту
3. Тестувати зміни перед комітом
4. Використовувати `.gitignore` для виключення непотрібних файлів
5. Документувати нові API endpoints через Swagger анотації

## 📖 Додаткова документація

- [Інструкція з деплою на Azure](AZURE_DEPLOYMENT.md) - детальний гайд для розгортання проекту на Microsoft Azure
- [Swagger/OpenAPI документація](http://localhost:5000/api/docs/) - інтерактивна документація API (після запуску)
