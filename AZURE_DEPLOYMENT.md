# 📘 Покрокова інструкція для деплою на Azure

Цей документ містить детальну інструкцію для розгортання Flask додатку на Microsoft Azure.

## 📋 Зміст

1. [Передумови](#передумови)
2. [Крок 1: Створення Azure MySQL Database](#крок-1-створення-azure-mysql-database)
3. [Крок 2: Створення Azure Web App](#крок-2-створення-azure-web-app)
4. [Крок 3: Налаштування змінних середовища](#крок-3-налаштування-змінних-середовища)
5. [Крок 4: Деплой коду](#крок-4-деплой-коду)
6. [Крок 5: Перевірка працездатності](#крок-5-перевірка-працездатності)
7. [Додаткові налаштування](#додаткові-налаштування)

---

## Передумови

Перед початком переконайтеся, що у вас є:

- ✅ Акаунт Microsoft Azure (безкоштовна підписка доступна за посиланням: https://azure.microsoft.com/free/)
- ✅ Встановлений Azure CLI (https://docs.microsoft.com/cli/azure/install-azure-cli)
- ✅ Встановлений Git
- ✅ Python 3.8 або вище
- ✅ Код проекту на GitHub

---

## Крок 1: Створення Azure MySQL Database

### 1.1. Вхід в Azure Portal

1. Перейдіть на https://portal.azure.com
2. Увійдіть за допомогою облікового запису Microsoft

### 1.2. Створення MySQL сервера

1. В Azure Portal натисніть **"Create a resource"**
2. Знайдіть **"Azure Database for MySQL Flexible Server"**
3. Натисніть **"Create"**

### 1.3. Налаштування сервера

**Вкладка Basics:**

- **Subscription**: Оберіть вашу підписку
- **Resource Group**: Створіть нову групу ресурсів або оберіть існуючу (наприклад, `myapp-rg`)
- **Server name**: Введіть унікальне ім'я (наприклад, `myapp-mysql-server`)
- **Region**: Оберіть найближчий регіон (наприклад, `West Europe`)
- **MySQL version**: 8.0 (рекомендовано)
- **Compute + Storage**: Оберіть **Burstable, B1ms** (найдешевший варіант для тестування)
- **Admin username**: Введіть ім'я адміністратора (наприклад, `dbadmin`)
- **Password**: Створіть надійний пароль (збережіть його!)

**Вкладка Networking:**

- **Connectivity method**: Public access
- **Firewall rules**:
  - Додайте правило: **Allow public access from any Azure service within Azure** (встановіть прапорець)
  - Додайте правило для вашого локального IP (для тестування): натисніть "Add current client IP address"

**Вкладка Security:**

- Залишіть налаштування за замовчуванням

4. Натисніть **"Review + create"**, потім **"Create"**
5. Зачекайте 5-10 хвилин до завершення створення

### 1.4. Створення бази даних

1. Після створення сервера перейдіть до нього
2. В лівому меню оберіть **"Databases"**
3. Натисніть **"+ Add"**
4. Введіть ім'я бази даних (наприклад, `database_lab1_eer`)
5. Оберіть **Charset**: `utf8mb4`
6. Оберіть **Collation**: `utf8mb4_general_ci`
7. Натисніть **"Save"**

### 1.5. Збережіть параметри підключення

Запишіть наступну інформацію (знадобиться пізніше):

```
DB_HOST: myapp-mysql-server.mysql.database.azure.com
DB_USER: dbadmin
DB_PASSWORD: ваш_пароль
DB_NAME: database_lab1_eer
```

---

## Крок 2: Створення Azure Web App

### 2.1. Створення Web App

1. В Azure Portal натисніть **"Create a resource"**
2. Знайдіть **"Web App"**
3. Натисніть **"Create"**

### 2.2. Налаштування Web App

**Вкладка Basics:**

- **Subscription**: Оберіть вашу підписку
- **Resource Group**: Оберіть ту саму, що й для MySQL
- **Name**: Унікальне ім'я для додатку (наприклад, `myapp-flask-api`)
- **Publish**: Code
- **Runtime stack**: Python 3.11
- **Operating System**: Linux
- **Region**: Той самий, що й MySQL сервер
- **App Service Plan**: Створіть новий або оберіть існуючий
  - **Pricing Plan**: Оберіть **Free F1** або **Basic B1** (для тестування)

**Вкладка Deployment:**

- **GitHub Actions settings**: Увімкніть (Enable)
- **GitHub account**: Авторизуйте GitHub
- **Organization**: Ваш GitHub аккаунт
- **Repository**: Оберіть репозиторій з вашим проектом
- **Branch**: main (або master)

**Вкладка Monitoring:**

- **Enable Application Insights**: Yes (рекомендовано для моніторингу)

3. Натисніть **"Review + create"**, потім **"Create"**

---

## Крок 3: Налаштування змінних середовища

### 3.1. Додавання змінних

1. Перейдіть до вашого Web App в Azure Portal
2. В лівому меню оберіть **"Configuration"** → **"Application settings"**
3. Натисніть **"+ New application setting"** та додайте наступні змінні:

```
DB_USER = dbadmin
DB_PASSWORD = ваш_mysql_пароль
DB_HOST = myapp-mysql-server.mysql.database.azure.com
DB_NAME = database_lab1_eer
FLASK_ENV = production
SECRET_KEY = згенеруйте_випадковий_ключ
```

### 3.2. Налаштування startup command

1. В розділі **"Configuration"** → **"General settings"**
2. В полі **"Startup Command"** введіть:

```bash
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

3. Натисніть **"Save"** і підтвердіть перезапуск

---

## Крок 4: Деплой коду

### Метод 1: GitHub Actions (Автоматичний - Рекомендовано)

Якщо ви увімкнули GitHub Actions під час створення Web App, Azure автоматично створив workflow файл у вашому репозиторії.

1. Внесіть зміни в код та зробіть commit
2. Push змін в GitHub:

```bash
git add .
git commit -m "Підготовка до Azure деплою"
git push origin main
```

3. Перейдіть на GitHub → ваш репозиторій → вкладка **"Actions"**
4. Слідкуйте за процесом деплою
5. Після завершення ваш додаток автоматично оновиться

### Метод 2: Azure CLI (Ручний)

```bash
# Увійдіть в Azure
az login

# Встановіть активну підписку
az account set --subscription "назва_вашої_підписки"

# Деплой з локального репозиторію
az webapp up --name myapp-flask-api --resource-group myapp-rg --runtime "PYTHON:3.11"
```

### Метод 3: Git Deploy (Локальний Git)

1. В Azure Portal → ваш Web App → **"Deployment Center"**
2. Оберіть **"Local Git"** як джерело
3. Натисніть **"Save"** і скопіюйте Git URL
4. На вашому локальному комп'ютері:

```bash
# Додайте Azure remote
git remote add azure <скопійований_git_url>

# Push код на Azure
git push azure main
```

---

## Крок 5: Перевірка працездатності

### 5.1. Ініціалізація бази даних

Якщо у вашому проекті є скрипт ініціалізації БД, виконайте його:

1. Перейдіть до Web App → **"SSH"** або **"Advanced Tools"** → **"Go"**
2. Відкрийте консоль
3. Виконайте команди:

```bash
cd /home/site/wwwroot
python my_project/db_init.py
```

### 5.2. Перевірка Swagger документації

1. Відкрийте браузер
2. Перейдіть на: `https://myapp-flask-api.azurewebsites.net/api/docs/`
3. Ви побачите інтерактивну Swagger документацію з усіма API endpoints

### 5.3. Тестування API endpoints

В Swagger UI спробуйте виконати запити:

**GET /users**

- Клацніть на endpoint
- Натисніть **"Try it out"**
- Натисніть **"Execute"**
- Перевірте відповідь

**POST /users** (створити користувача)

```json
{
  "name": "Тестовий Користувач",
  "email": "test@example.com"
}
```

**GET /categories** - отримати всі категорії

**GET /properties** - отримати всі властивості

### 5.4. Тестування з локального ПК через Postman або curl

```bash
# GET запит
curl https://myapp-flask-api.azurewebsites.net/users

# POST запит
curl -X POST https://myapp-flask-api.azurewebsites.net/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Іван Петренко","email":"ivan@example.com"}'
```

---

## Додаткові налаштування

### Моніторинг логів

1. Azure Portal → ваш Web App → **"Log stream"**
2. Переглядайте логи в реальному часі

Або через Azure CLI:

```bash
az webapp log tail --name myapp-flask-api --resource-group myapp-rg
```

### Налаштування custom domain

1. Web App → **"Custom domains"**
2. Додайте ваш домен
3. Налаштуйте SSL сертифікат

### Автоматичне масштабування

1. Web App → **"Scale up (App Service plan)"**
2. Оберіть вищий тарифний план
3. Web App → **"Scale out (App Service plan)"**
4. Налаштуйте правила автомасштабування

### Backup бази даних

1. MySQL Server → **"Backups"**
2. Azure автоматично створює backup
3. Можна відновити на будь-яку точку часу

---

## 🔍 Перевірка для здачі лабораторної

**Перевірте наступне:**

✅ **Код на GitHub:**

- Репозиторій публічний або викладач має доступ
- Всі файли закомічені
- README.md оновлений

✅ **Azure MySQL:**

- База даних створена і працює
- Таблиці ініціалізовані
- З'єднання налаштоване

✅ **Azure Web App:**

- Додаток запущений
- Swagger документація доступна
- URL працює: `https://ваш-додаток.azurewebsites.net/api/docs/`

✅ **REST API працює:**

- GET /users повертає дані
- POST /users створює користувача
- GET /categories працює
- GET /properties працює
- GET /property-categories працює

✅ **Тестування з локального ПК:**

- curl або Postman запити працюють
- Відповіді приходять у JSON форматі

---

## 🆘 Вирішення проблем

### Проблема: "Application Error"

**Рішення:**

1. Перевірте логи: `az webapp log tail`
2. Перевірте змінні середовища в Configuration
3. Перевірте startup command

### Проблема: "Can't connect to MySQL server"

**Рішення:**

1. Перевірте firewall rules в MySQL сервері
2. Увімкніть "Allow Azure services"
3. Перевірте правильність DB_HOST (має бути повний hostname)

### Проблема: "Module not found"

**Рішення:**

1. Перевірте requirements.txt
2. Переконайтеся, що gunicorn встановлений
3. Перезапустіть Web App

### Проблема: Swagger не відображається

**Рішення:**

1. Перевірте, що flasgger встановлений
2. Перевірте URL: `/api/docs/` (з слешем в кінці)
3. Очистіть кеш браузера

---

## 📚 Корисні посилання

- Azure Portal: https://portal.azure.com
- Azure CLI Documentation: https://docs.microsoft.com/cli/azure/
- Azure App Service Python: https://docs.microsoft.com/azure/app-service/quickstart-python
- Azure MySQL: https://docs.microsoft.com/azure/mysql/
- Flasgger Documentation: https://github.com/flasgger/flasgger
- Flask Documentation: https://flask.palletsprojects.com/

---

## 💰 Вартість

**Для студентів:**

- Azure for Students: $100 безкоштовних кредитів (не потрібна кредитна картка)
- Безкоштовний план (F1) Web App
- Базовий план MySQL (може бути платним, але дуже дешевий ~$15/місяць)

**Порада:** Після здачі лабораторної видаліть ресурси, щоб не витрачати кредити!

```bash
# Видалити всю resource group (обережно!)
az group delete --name myapp-rg --yes
```

---

**Успіхів з деплоєм! 🚀**
