# Database Project

Flask проект з базою даних для управління користувачами, категоріями та властивостями.

## Встановлення та налаштування

### 1. Клонування репозиторію
```bash
git clone <URL_РЕПОЗИТОРІЮ>
cd database-main
```

### 2. Створення віртуального середовища
```bash
python3 -m venv venv_new
source venv_new/bin/activate  # На macOS/Linux
# або
venv_new\Scripts\activate     # На Windows
```

### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 4. Налаштування бази даних
Відредагуйте файл `config/app.yml` з вашими налаштуваннями бази даних:
```yaml
db:
  host: localhost
  user: your_username
  password: your_password
  database: your_database_name
  charset: utf8mb4
```

### 5. Запуск додатку
```bash
python app.py
```

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

## API Endpoints

- `/users` - Управління користувачами
- `/categories` - Управління категоріями
- `/properties` - Управління властивостями
- `/property-categories` - Зв'язки між властивостями та категоріями

## Технології

- **Flask** - Web фреймворк
- **SQLAlchemy** - ORM для роботи з базою даних
- **PyMySQL** - MySQL драйвер для Python
- **PyYAML** - Парсинг конфігураційних файлів

## Розробка

Для розробки рекомендується:
1. Використовувати віртуальне середовище
2. Дотримуватися структури проекту
3. Тестувати зміни перед комітом
4. Використовувати `.gitignore` для виключення непотрібних файлів
