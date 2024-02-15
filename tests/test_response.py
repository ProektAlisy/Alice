from http import HTTPStatus

from fastapi.testclient import TestClient

from app.main import application

client = TestClient(application)


def test_root_endpoint():
    """
    Тест для проверки работы эндпоинта.
    :return:
    """
    request_data_new_session = {
        "session": {"new": True},
        "request": {"command": "some_command"},
        "state": None,
    }
    response_new_session = client.post("/", json=request_data_new_session)
    assert response_new_session.status_code == HTTPStatus.OK
    assert "response" in response_new_session.json()
    assert "text" in response_new_session.json()["response"]
    assert "end_session" in response_new_session.json()["response"]
    assert "session_state" in response_new_session.json()

    # Тест для случая, когда сессия уже существует
    request_data_existing_session = {
        "session": {"new": False},
        "request": {"command": "some_command"},
        "state": None,
    }
    response_existing_session = client.post(
        "/", json=request_data_existing_session,
    )
    assert response_existing_session.status_code == HTTPStatus.OK
    assert "response" in response_existing_session.json()
    assert "text" in response_existing_session.json()["response"]
    assert "end_session" in response_existing_session.json()["response"]
    assert "session_state" in response_existing_session.json()


def test_root_endpoint_with_state():
    """
    Тест для проверки работы эндпоинта с сохраненным состоянием.
    :return:
    """
    request_data = {
        "session": {"new": False},
        "request": {"command": "some_command"},
        "state": {"session": {"key": "value"}},
    }
    response = client.post("/", json=request_data)
    assert response.status_code == HTTPStatus.OK
    assert "response" in response.json()
    assert "text" in response.json()["response"]
    assert "end_session" in response.json()["response"]
    assert "session_state" in response.json()


def test_root_endpoint_intents():
    """
    Тест для проверки работы эндпоинта с интентами.
    :return:
    """
    request_data = {
        "session": {"new": False},
        "request": {"command": "some_command",
                    "nlu": {"intents": ["intent1", "intent2"]},
                    },
        "state": None,
    }
    response = client.post("/", json=request_data)
    assert response.status_code == HTTPStatus.OK
    assert "response" in response.json()
    assert "text" in response.json()["response"]
    assert "end_session" in response.json()["response"]
    assert "session_state" in response.json()
