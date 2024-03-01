import pytest


@pytest.fixture
def data():
    return {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
        },
        "session": {
            "new": True,
        },
        "request": {
            "command": "",
            "original_utterance": "Прослушать информацию об учебно-кинологическом центре собаки-помощники",
            "nlu": {"tokens": [], "entities": [], "intents": {}},
            "type": "SimpleUtterance",
        },
        "state": {"session": {}, "user": {}, "application": {}},
        "version": "1.0",
    }
