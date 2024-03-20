from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from app.constants.comands_states_answers import (
    COMMANDS_STATES_ANSWERS_INTENTS,
    after_answers_documents,
    another_answers_documents,
    answers_documents,
)
from app.constants.commands import Commands, ServiceCommands
from app.constants.states import STATES
from app.core.utils import (
    compose_message,
    get_after_answer_by_state,
    get_answer_by_state,
)
from app.main import application
from app.skill import skill

client = TestClient(application)


def test_direct_commands(data, load_session_state_mock):
    """Тест базового сценария навыка.

    После старта навыка пользователь по порядку обращается прямым запросом ко
    всем историям навыка, кроме "take_quiz" и "take_manual_training".

    Args:
        data: Данные для запроса.
        load_session_state_mock: Мокнутая функция `load_session_state`.
    """
    response = client.post("/", json=data)
    assert response.status_code == HTTP_200_OK, "Status code is not 200"
    assert response.json()["response"]["text"] == another_answers_documents.get(
        "full_greetings",
    ), "Key value mismatch in response"
    data["session"]["new"] = False
    command_names = Commands.__annotations__
    state_to_remove = [
        "TAKE_QUIZ",
        "TAKE_MANUAL_TRAINING",
    ]
    command_names = {
        key: value for key, value in command_names.items() if key not in state_to_remove
    }

    for command_name in command_names:
        data["request"]["command"] = getattr(Commands, command_name).lower()
        load_session_state_mock()
        response = client.post("/", json=data)
        assert response.status_code == HTTP_200_OK, "Status code is not 200"
        if command_name == "INSTRUCTIONS_FOR_LAUNCHING_PODCAST":
            true_answer = compose_message(
                answers_documents.get(
                    "instructions_for_launching_podcast",
                    "",
                ),
                after_answers_documents.get("about_training_course", ""),
            )
        else:
            true_answer = compose_message(
                answers_documents.get(command_name.lower(), ""),
                after_answers_documents.get(command_name.lower(), ""),
            )

        assert (
            response.json()["response"]["text"][:1009] == true_answer[:1009]
        ), "Key value mismatch in response"


def test_agree_commands(data, load_session_state_mock):
    """Тест `agree` сценария навыка.

    После старта навыка пользователь соглашается с предложениями навыка,
    кроме "take_quiz" и "take_manual_training".

    Args:
        data: Данные для запроса.
        load_session_state_mock: Мокнутая функция `load_session_state`.
    """
    skill.history = []
    skill.progress = []

    data["session"]["new"] = False
    for state in STATES[1:]:
        data["request"]["command"] = ServiceCommands.AGREE[0]
        if state in [
            "take_quiz",
            "take_manual_training",
        ]:
            data["request"]["command"] = ServiceCommands.DISAGREE[0]
            client.post("/", json=data)
            continue
        if state == "instructions_for_launching_podcast":
            true_answer = compose_message(
                answers_documents.get(
                    "instructions_for_launching_podcast",
                    "",
                ),
                after_answers_documents.get("about_training_course", ""),
            )
        else:
            true_answer = compose_message(
                get_answer_by_state(state, COMMANDS_STATES_ANSWERS_INTENTS),
                get_after_answer_by_state(
                    state,
                    COMMANDS_STATES_ANSWERS_INTENTS,
                ),
            )
        load_session_state_mock()
        response = client.post("/", json=data)
        assert response.status_code == HTTP_200_OK, "Status code is not 200"
        assert (
            response.json()["response"]["text"][:1009] == true_answer[:1009]
        ), "Key value mismatch in response"
