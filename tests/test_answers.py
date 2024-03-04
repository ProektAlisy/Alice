from icecream import ic
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from app.constants.comands_states_answers import (
    another_answers_documents,
    answers_documents,
    after_answers_documents,
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
    data["session"]["new"] = False
    states = Commands.__annotations__
    state_to_remove = [
        "TAKE_QUIZ",
        "TAKE_MANUAL_TRAINING",
        "HELP_MAIN",
        "HELP_PHRASE",
        "POSSIBILITIES",
        "USEFUL_INFORMATION",
    ]
    states = {
        key: value
        for key, value in states.items()
        if key not in state_to_remove
    }
    for field in states:
        data["request"]["command"] = getattr(Commands, field).lower()
        response = client.post("/", json=data)
        assert response.status_code == HTTP_200_OK, "Status code is not 200"
        true_answer = (
            answers_documents.get(field.lower())
            + " sil<[400]> "
            + after_answers_documents.get(field.lower())
        )
        assert (
            response.json()["response"]["text"][:1009] == true_answer[:1009]
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
