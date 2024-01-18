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

`pip install -r requirements.txt`

- Запустить проект:
```
uvicorn app.main:app --reload
```
