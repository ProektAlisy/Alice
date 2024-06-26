import pytest

from app.machine import FiniteStateMachine
from app.skill import skill


@pytest.fixture(scope="function")
def load_session_state_mock(mocker):
    return mocker.patch.object(
        FiniteStateMachine,
        "load_session_state",
        return_value=skill.progress,
    )


@pytest.fixture(scope="function")
def data():
    return {
        "session": {
            "new": True,
        },
        "request": {
            "command": "",
            "nlu": {"tokens": [], "entities": [], "intents": {}},
            "type": "SimpleUtterance",
        },
        "state": {"session": {}, "user": {}, "application": {}},
        "version": "1.0",
    }
