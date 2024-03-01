from icecream import ic
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from app.constants.comands_states_answers import (
    another_answers_documents,
    answers_documents,
)
from app.constants.commands import Commands
from app.main import application
from tests.fixtures.answers_fixtures import data

client = TestClient(application)


def test_root(data):
    response = client.post("/", json=data)

    assert response.status_code == HTTP_200_OK, "Status code is not 200"
    assert response.json()["response"][
        "text"
    ] == another_answers_documents.get(
        "full_greetings"
    ), "Key value mismatch in response"
    for field in Commands.__annotations__:
        print(field)
        print(answers_documents.get(field.lower()))
        print(getattr(Commands, field), "555")
        # data["request"]["command"] = getattr(Commands, field)
        # data["request"]["original_utterance"] = getattr(Commands, field)
        response = client.post("/", json=data)

        assert response.status_code == HTTP_200_OK, "Status code is not 200"
        assert response.json()["response"]["text"] == answers_documents.get(
            field.lower()
        ), "Key value mismatch in response"


#
# def test_ok_answer(data):
#     for field in Commands.__annotations__:
#         print(field)
#         print(answers_documents.get(field.lower()))
#         print(getattr(Commands, field), "555")
#         data["request"]["command"] = getattr(Commands, field)
#         ic(data)
#         response = client.post("/", json=data)
#
#         assert response.status_code == HTTP_200_OK, "Status code is not 200"
#         assert response.json()["response"]["text"] == answers_documents.get(
#             field.lower()
#         ), "Key value mismatch in response"
