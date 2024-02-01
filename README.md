# Alice
Навык для голосового помощника Алиса

ProjectTree.theme

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

`pip install -r requirements.txt`

- Создать туннель ngrok:
```
ngrok http 8000
```
- Запустить MongoDB.

- Запустить проект:
```
uvicorn app.main:application --reload
```
- Скопировать временный URL из ngrok и вставить его в настройки навыка Яндекс.Диалоги(Webhook URL)