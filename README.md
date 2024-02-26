# Alice
Навык для голосового помощника Алиса

### Запуск проекта локально:

- В дирректории `Alice/` создать виртуальное окружение:

`python -m venv venv`

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

- Создание и запуск проект через Docker-Compose (нужно находится в папке /infra):
```
docker-compose up -d --build
```
- Скопировать временный URL из ngrok и вставить его в настройки навыка Яндекс.Диалоги(Webhook URL)
```
scp -r infra/* root@80.87.108.69:/home/alice_app/
```

- Деплой происходит при команде git push.
- Предварительно проходит проверка flake8 и автотесты.