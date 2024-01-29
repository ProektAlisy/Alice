from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import application

client = TestClient(application)


def test_root_endpoint():
    """
    Проверяет доступность эндпоинта.
    """
    request_data = {
        "session": {"new": True},
        "request": {"command": ""},
    }
    response = client.post("/", json=request_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "response" in data
    assert "text" in data["response"]
    assert "end_session" in data["response"]


def test_request_response():
    """
    Проверяет что текст из реквеста возвращается в респонс.
    """
    request_data = {
        "session": {"new": True},
        "request": {"command": " Привет!"},
    }
    response = client.post("/", json=request_data)
    data = response.json()
    assert "response" in data
    assert "text" in data["response"]
    assert "end_session" in data["response"]


def test_exit_command():
    """
    Проверка комманды выхода.
    """
    request_data = {
        "session": {"new": True},
        "request": {"command": "выход"},
    }
    response = client.post("/", json=request_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "response" in data
    assert "text" in data["response"]
    assert "end_session" in data["response"]
    assert data["response"]["end_session"] is True
