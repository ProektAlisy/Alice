[![Alice-app workflow](https://github.com/ProektAlisy/Alice/actions/workflows/main.yml/badge.svg)](https://github.com/ProektAlisy/Alice/actions/workflows/main.yml)
# Alice
Навык для голосового помощника Алиса

### Запуск проекта локально:

- В директории `Alice/` создать виртуальное окружение:
```
python -m venv venv
```
- Активировать виртуальное окружение:

  * Если у вас Linux/macOS:
    ```
    source venv/bin/activate
    ```
  * Если у вас windows:
    ```
    source venv/scripts/activate
    ```

- Установить зависимости:
```
pip install -r requirements.txt
```
- Создать туннель ngrok:
```
ngrok http 8000
```
- Запустить MongoDB.
- Наполнить БД ответами пользователю:
```
python db_loader.py
```
- Запустить проект:
```
uvicorn app.main:application --reload
```

## Запуск проекта локально через docker-compose:

### Шаблон наполнения env-файла:
```
MONGO_TEST_HOST="localhost"
MONGO_TEST_USER="root"
MONGO_TEST_PASSWORD="example"
ME_CONFIG_MONGODB_ADMINUSERNAME="adminuser"
ME_CONFIG_MONGODB_ADMINPASSWORD="adminpassword"
ME_CONFIG_MONGODB_URL="www.guidedogs.acceleratorpracticum.ru"
MONGO_INITDB_ROOT_USERNAME="adminuser"
MONGO_INITDB_ROOT_PASSWORD="adminpassword"
MONGO_PORT="27017"
SENTRY_DSN="https://somedsn"
```


### Как запустить проект:
Клонируем репозиторий:
```
git clone https://github.com/ProektAlisy/Alice.git
```
Переходим в директорию с файлом docker_compose.yaml:
```
cd infra
```
Собираем контейнеры и запускаем их:
```
docker-compose up -d --build 
```
Наполняем базу данных:
```
sudo docker exec alice_app-app-1 python app/monga/db_loader.py
```

## Запуск проекта на сервере через docker-compose и GitHub Actions:
Копируем файлы docker-compose и конфигурации nginx выполнив команду:
```
scp -r infra/* username@server:/home/alice_app/
```

### Используя этот шаблон наполнения env-файла прописываем константы в GitHub Actions:
```
MONGO_TEST_HOST="localhost"
MONGO_TEST_USER="root"
MONGO_TEST_PASSWORD="example"
ME_CONFIG_MONGODB_ADMINUSERNAME="adminuser"
ME_CONFIG_MONGODB_ADMINPASSWORD="adminpassword"
ME_CONFIG_MONGODB_URL="www.guidedogs.acceleratorpracticum.ru"
MONGO_INITDB_ROOT_USERNAME="adminuser"
MONGO_INITDB_ROOT_PASSWORD="adminpassword"
MONGO_PORT="27017"
SENTRY_DSN="https://somedsn"
```

- Автоматический деплой происходит при команде git push в ветку develop или main.
- Предварительно проходит проверка flake8 и автотесты.
- Базы данных наполнятся автоматически.

## Если автоматического развёртывания не произошло:
Копируем проект:
```
git clone https://github.com/ProektAlisy/Alice.git
```
Копируем файлы docker-compose и конфигурации nginx выполнив команду:
```
scp -r infra/* username@server:/home/alice_app/
```
Переходим на сервере в папку c docker-compose:
```
cd ..
cd home/alice_app/
```
Запускаем приложение командой:
```
docker-compose up -d --build
```
Наполняем базу данных:
```
sudo docker exec alice_app-app-1 python app/monga/db_loader.py
```
Проверить запущенные контейнеры можно командой:
```
docker-compose ps
```

Если поменяется домен, то необходимо изменить домен в файле settings.py:
```
BASE_AUDIO_URL = "https://www.new_addres.ru/"
```

## Получение сертификата при смене домена

Чтобы начать процесс получения сертификата, введите команду:
```
sudo certbot --nginx 
```

В процессе оформления сертификата вам нужно будет указать свою электронную почту и ответить на несколько вопросов.

- "Enter email address" (англ. «введите почту»). Почта нужна для предупреждений, что сертификат пора обновить.
- "Please read the Terms of Service..." (англ. «прочитайте правила сервиса»). Прочитайте правила по ссылке, введите y и нажмите Enter.
- "Would you be willing to share your email address with the Electronic Frontier Foundation?" (англ. «хотите ли вы поделиться своей почтой с Фондом электронных рубежей»). Отметьте на своё усмотрение y (да) или n (нет) и нажмите Enter.
- "Please enter the domain name(s) you would like on your certificate" (англ. «пожалуйста, введите доменные имена, которые вы хотели бы видеть в своем сертификате»). Введите добавленное в проект доменное имя, нажмите Enter.

После этого certbot отправит ваши данные на сервер Let's Encrypt и там будет выпущен сертификат, который автоматически сохранится на вашем сервере. Также будет изменена конфигурация вашего nginx: добавятся нужные настройки и будут прописаны пути к сертификату.
Перезапустите nginx:
```
sudo systemctl reload nginx 
```
Зайдите через браузер на свой проект. Теперь в адресной строке вместо HTTP будет указан протокол HTTPS (англ. HyperText Transfer Protocol Secure), а рядом с адресом будет виден символ «замочек». Это значит, что сертификат успешно подключён и информация между клиентом и сервером передаётся в зашифрованном виде. Клик по замочку покажет подробную информацию о сертификате.

# Обновление сертификата

Бесплатный сертификат нужно обновлять минимум раз в три месяца. Certbot делает это по умолчанию, если вы не меняли стандартных настроек. 
Убедиться, что всё обновляется, можно с помощью команды:
```
sudo certbot renew --dry-run 
```
Если по каким-то причинам автообновление не происходит, то можно выполнить следующую команду:
```
sudo certbot renew --pre-hook "service nginx stop" --post-hook "service nginx start" 
```
Эта команда обновит сертификат и перезапустит nginx.
