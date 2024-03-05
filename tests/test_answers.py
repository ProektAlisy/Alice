from icecream import ic
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from app.constants.comands_states_answers import (
    another_answers_documents,
    answers_documents,
    after_answers_documents,
)
from app.constants.commands import Commands
from app.constants.states import STATES
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
    command_names = Commands.__annotations__
    state_to_remove = [
        "TAKE_QUIZ",
        "TAKE_MANUAL_TRAINING",
    ]
    command_names = {
        key: value
        for key, value in command_names.items()
        if key not in state_to_remove
    }
    for command_name in command_names:
        data["request"]["command"] = getattr(Commands, command_name).lower()
        response = client.post("/", json=data)
        assert response.status_code == HTTP_200_OK, "Status code is not 200"
        if command_name == "INSTRUCTIONS_FOR_LAUNCHING_PODCAST":
            true_answer = (
                answers_documents.get("instructions_for_launching_podcast")
                + " sil<[400]> "
                + after_answers_documents.get("about_training_course")
            )
        else:
            true_answer = (
                answers_documents.get(command_name.lower())
                + " sil<[400]> "
                + after_answers_documents.get(command_name.lower())
            )
        assert (
            response.json()["response"]["text"][:1009] == true_answer[:1009]
        ), "Key value mismatch in response"
