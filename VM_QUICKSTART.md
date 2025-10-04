# 🚀 Швидкий старт: Деплой на Azure VM

## Для студентів - мінімальні кроки

### Крок 1: Створення MySQL бази даних (5 хвилин)

1. Перейдіть на https://portal.azure.com
2. **Create a resource** → шукайте **"MySQL"**
3. Оберіть **"Azure Database for MySQL Flexible Server"**
4. Налаштуйте:
   - Resource group: створіть нову `myapp-rg`
   - Server name: `ваше-імя-mysql` (має бути унікальним)
   - Region: `West Europe`
   - Compute + Storage: **Burstable, B1ms** (найдешевший)
   - Admin username: `dbadmin`
   - Password: **ЗАПИШІТЬ ЦЕЙ ПАРОЛЬ!**
5. Networking → Allow public access → встановіть прапорець
6. **Create**
7. Після створення → Databases → Add → назва: `database_lab1_eer`

**ЗБЕРЕЖІТЬ:**

```
Host: ваше-імя-mysql.mysql.database.azure.com
User: dbadmin
Password: ваш_пароль
Database: database_lab1_eer
```

---

### Крок 2: Створення віртуальної машини (5 хвилин)

1. Azure Portal → **Create a resource** → **"Virtual Machine"**
2. Налаштуйте:
   - Resource group: оберіть `myapp-rg` (ту саму)
   - Name: `myapp-vm`
   - Region: `West Europe` (той самий!)
   - Image: **Ubuntu Server 22.04 LTS**
   - Size: **Standard_B1s** (найдешевший) або **B2s**
   - Authentication: **SSH public key**
   - Username: `azureuser`
   - SSH key: **Generate new key pair** → назва: `myapp-vm-key`
3. Disks → OS disk type: **Standard SSD**
4. Networking:
   - Public inbound ports: **Allow selected ports**
   - Select: **SSH (22), HTTP (80), HTTPS (443)**
5. **Create**
6. **ВАЖЛИВО:** Завантажте приватний SSH ключ коли з'явиться вікно!

**ЗБЕРЕЖІТЬ:**

- SSH ключ (файл .pem)
- Public IP адресу VM (знайдете на сторінці VM після створення)

---

### Крок 3: Підключення до VM (2 хвилини)

На вашому комп'ютері:

**macOS/Linux:**

```bash
# Налаштуйте права доступу
chmod 400 ~/Downloads/myapp-vm-key.pem

# Підключіться
ssh -i ~/Downloads/myapp-vm-key.pem azureuser@ваш_public_ip
```

**Windows (PowerShell):**

```powershell
ssh -i C:\Users\ВашеІмя\Downloads\myapp-vm-key.pem azureuser@ваш_public_ip
```

Якщо запитає "Are you sure?", введіть `yes`

---

### Крок 4: Налаштування середовища (10 хвилин)

На VM виконайте команди вручну:

#### 4.1. Оновлення системи

```bash
sudo apt update
sudo apt upgrade -y
```

#### 4.2. Встановлення необхідного ПЗ

```bash
# Python та інструменти
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx

# Додаткові бібліотеки
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev mysql-client
```

#### 4.3. Клонування проекту

```bash
cd ~
git clone https://github.com/ваш_username/ваш_репозиторій.git
cd назва_репозиторію
```

#### 4.4. Віртуальне середовище

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4.5. Створення .env файлу

```bash
nano .env
```

Додайте (замініть на ваші значення):

```env
DB_USER=dbadmin
DB_PASSWORD=ваш_пароль_з_кроку_1
DB_HOST=ваше-імя-mysql.mysql.database.azure.com
DB_NAME=database_lab1_eer
FLASK_ENV=production
SECRET_KEY=any_random_secret_key_here
```

Збережіть: `Ctrl+O`, `Enter`, `Ctrl+X`

#### 4.6. Налаштування Nginx

```bash
# Створіть конфігурацію
sudo nano /etc/nginx/sites-available/flask-app
```

Додайте:

```nginx
server {
    listen 80;
    server_name ваш_public_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /flasgger_static/ {
        proxy_pass http://127.0.0.1:8000/flasgger_static/;
    }
}
```

Збережіть та активуйте:

```bash
sudo ln -s /etc/nginx/sites-available/flask-app /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

#### 4.7. Налаштування systemd service

```bash
sudo nano /etc/systemd/system/flask-app.service
```

Додайте (замініть шляхи):

```ini
[Unit]
Description=Flask Application
After=network.target

[Service]
User=azureuser
Group=www-data
WorkingDirectory=/home/azureuser/назва_репозиторію
Environment="PATH=/home/azureuser/назва_репозиторію/venv/bin"
EnvironmentFile=/home/azureuser/назва_репозиторію/.env
ExecStart=/home/azureuser/назва_репозиторію/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 --timeout 600 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустіть:

```bash
sudo systemctl daemon-reload
sudo systemctl start flask-app
sudo systemctl enable flask-app
sudo systemctl status flask-app
```

---

### Крок 5: Перевірка (2 хвилини)

#### На VM:

```bash
# Перевірте статус
sudo systemctl status flask-app

# Перевірте локально
curl http://localhost/users
```

#### З вашого комп'ютера:

```bash
# В браузері відкрийте:
http://ваш_public_ip/api/docs/

# Або в терміналі:
curl http://ваш_public_ip/users
```

---

## ✅ Готово для здачі!

Тепер у вас є:

- ✅ Код на GitHub
- ✅ Azure MySQL Database
- ✅ Azure VM з запущеним додатком
- ✅ Swagger документація доступна онлайн
- ✅ REST API працює

---

## 🔧 Корисні команди

### На VM:

```bash
# Перегляд логів
sudo journalctl -u flask-app -f

# Перезапуск додатку
sudo systemctl restart flask-app

# Статус сервісів
sudo systemctl status flask-app
sudo systemctl status nginx

# Оновлення коду з GitHub
cd ~/назва_проекту
git pull origin main
sudo systemctl restart flask-app
```

### З локального ПК:

```bash
# Підключення до VM
ssh -i myapp-vm-key.pem azureuser@ваш_ip

# Тестування API
curl http://ваш_ip/users
curl http://ваш_ip/categories
curl http://ваш_ip/properties

# Створення користувача
curl -X POST http://ваш_ip/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

---

## 🆘 Якщо щось не працює

### Додаток не запускається

```bash
# Подивіться що не так
sudo journalctl -u flask-app -n 50

# Спробуйте запустити вручну
cd ~/назва_проекту
source venv/bin/activate
python app.py
```

### MySQL не підключається

```bash
# Перевірте з VM
mysql -h your-mysql.mysql.database.azure.com -u dbadmin -p

# Якщо не працює:
# 1. Перевірте firewall rules в Azure Portal → MySQL → Networking
# 2. Додайте правило: 0.0.0.0 - 255.255.255.255
```

### 502 Bad Gateway

```bash
# Перезапустіть все
sudo systemctl restart flask-app
sudo systemctl restart nginx
```

---

## 💰 Вартість

- VM B1s: ~$7-10/міс
- MySQL B1ms: ~$15-20/міс
- **Загалом: ~$25-30/міс**

**Студенти отримують $100 безкоштовно!**

Після здачі видаліть ресурси:

1. Azure Portal → Resource groups
2. Оберіть `myapp-rg`
3. **Delete resource group**

---

## 📚 Повна документація

Для детальної інформації дивіться:

- [AZURE_VM_DEPLOYMENT.md](AZURE_VM_DEPLOYMENT.md) - повна інструкція
- [README.md](README.md) - загальна інформація про проект

---

**Успіхів! 🎉**
