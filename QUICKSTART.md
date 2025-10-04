# 🚀 Швидкий старт для деплою на Azure

## Перед деплоєм
1. ✅ Переконайтесь, що код на GitHub
2. ✅ Створіть акаунт Azure (безкоштовно для студентів)

## Швидкі команди

### Встановити Azure CLI (якщо ще не встановлено)
```bash
# macOS
brew install azure-cli

# Windows
# Завантажте з: https://aka.ms/installazurecliwindows
```

### Логін в Azure
```bash
az login
```

### Деплой одною командою (після створення ресурсів в Portal)
```bash
az webapp up \
  --name your-app-name \
  --resource-group your-rg \
  --runtime "PYTHON:3.11" \
  --location westeurope
```

## Основні URL після деплою

- **Ваш додаток:** `https://your-app-name.azurewebsites.net`
- **Swagger документація:** `https://your-app-name.azurewebsites.net/api/docs/`
- **OpenAPI spec:** `https://your-app-name.azurewebsites.net/apispec.json`

## Змінні середовища для Azure

В Azure Portal → Web App → Configuration → Application settings:

```
DB_USER = ваш_mysql_користувач
DB_PASSWORD = ваш_mysql_пароль
DB_HOST = ваш-mysql-сервер.mysql.database.azure.com
DB_NAME = назва_бази_даних
FLASK_ENV = production
```

## Startup Command для Azure Web App

```bash
gunicorn --bind=0.0.0.0:8000 --timeout 600 app:app
```

## Перевірка працездатності

```bash
# Тестування з командного рядка
curl https://your-app-name.azurewebsites.net/users

# Або відкрийте в браузері
https://your-app-name.azurewebsites.net/api/docs/
```

## Моніторинг логів

```bash
az webapp log tail \
  --name your-app-name \
  --resource-group your-rg
```

## 📚 Повна інструкція

Детальна покрокова інструкція доступна в [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)

