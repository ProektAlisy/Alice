import json
import uuid

import pytest

from app.constants.manual_training_player.intents import ManualTrainingIntents
from app.constants.manual_training_player.manual_training_messages import (
    ManualPlayerMessages,
)
from app.manual_training_player.manual_training_player import (
    WELCOME_TEXT,
    ManualTrainingPlayer,
)


@pytest.fixture
def manual_player():
    return ManualTrainingPlayer()


@pytest.fixture
def manual_player_with_chapter():
    player = ManualTrainingPlayer()
    player.greetings = True
    player.is_playing = True
    player.current_chapter = "1"
    if player.current_chapter not in player.token_offsets:
        player.token_offsets[player.current_chapter] = {
            "token": str(uuid.uuid4()),
            "offset_ms": 0,
        }
    return player


@pytest.fixture
def welcome_text():
    with open(WELCOME_TEXT, "r", encoding="utf-8") as file:
        welcome_data = json.load(file)
    return welcome_data["welcome_text"]


def test_process_request_greetings(manual_player, welcome_text):
    response, _ = manual_player.process_request("", [])
    assert response == welcome_text
    assert manual_player.greetings is True
    assert manual_player.is_finish is False


def test_process_request_play(manual_player):
    manual_player.greetings = True
    response, _ = manual_player.process_request(
        "",
        [ManualTrainingIntents.START_MANUAL_TRAINING],
    )
    assert response == ManualPlayerMessages.PLAYBACK_START.format(
        chapter_number="1",
        chapter_name="Вступление",
    )
    assert manual_player.is_playing is True
    assert (
        manual_player.start_audio_playback("1")[-1]["audio_player"]["item"][
            "stream"
        ]["url"]
        == "https://www.guidedogs.acceleratorpracticum.ru/00-vstuplenie.mp3"
    )


def test_process_request_pause(manual_player_with_chapter):
    manual_player_with_chapter.start_audio_playback("1")
    response, _ = manual_player_with_chapter.process_request(
        "",
        [ManualTrainingIntents.PAUSE_MANUAL_TRAINING],
    )
    assert response == ManualPlayerMessages.PLAYBACK_STOP
    assert manual_player_with_chapter.is_playing is False


def test_process_request_resume(manual_player_with_chapter):
    response, _ = manual_player_with_chapter.process_request(
        "",
        [ManualTrainingIntents.RESUME_MANUAL_TRAINING],
    )
    assert response == ManualPlayerMessages.PLAYBACK_START.format(
        chapter_number="1",
        chapter_name="Вступление",
    )
    assert manual_player_with_chapter.is_playing is True
    assert manual_player_with_chapter.greetings is True


def test_pause_resume_after_5_seconds(manual_player_with_chapter):
    chapter_number = manual_player_with_chapter.current_chapter
    manual_player_with_chapter.token_offsets[chapter_number][
        "offset_ms"
    ] = 5000
    manual_player_with_chapter.start_audio_playback(chapter_number)
    response1, _ = manual_player_with_chapter.process_request(
        "",
        {"pause_manual_training"},
    )
    assert response1 == ManualPlayerMessages.PLAYBACK_STOP
    assert manual_player_with_chapter.is_playing is False
    response2, directives2 = manual_player_with_chapter.process_request(
        "",
        {"resume_manual_training"},
    )
    offset_ms2 = directives2["audio_player"]["item"]["stream"]["offset_ms"]
    assert response2 == ManualPlayerMessages.PLAYBACK_START.format(
        chapter_number="1",
        chapter_name="Вступление",
    )
    assert offset_ms2 == 5000
    assert manual_player_with_chapter.is_playing is True


def test_get_chapter_info_empty(manual_player_with_chapter):
    response, _ = manual_player_with_chapter.process_request(
        "расскажи название главы",
        {
            "get_manual_training_chapter_info": {
                "slots": {"chapter": {"value": ""}},
            },
        },
    )
    assert response == ManualPlayerMessages.NO_CHAPTER_NUMBER


def test_get_chapter_info_with_incorrect_value(manual_player_with_chapter):
    response, _ = manual_player_with_chapter.process_request(
        "расскажи название главы 56",
        {
            "get_manual_training_chapter_info": {
                "slots": {"chapter": {"value": "56"}},
            },
        },
    )
    assert response == ManualPlayerMessages.CHAPTER_NUMBER_NOT_FOUND


def test_terminate_training(manual_player_with_chapter):
    response, _ = manual_player_with_chapter.process_request(
        "Остановить обучение по методичке",
        {"terminate_manual_training"},
    )
    assert response == ManualPlayerMessages.TRAINING_COMPLETED


def test_training_finished(manual_player):
    manual_player.greetings = True
    manual_player.current_chapter = "13"
    manual_player.start_audio_playback(manual_player.current_chapter)
    assert manual_player.current_chapter == "13"
    response, _ = manual_player.process_request(
        "следующая",
        {"next_manual_training_chapter"},
    )
    assert  manual_player.is_finish is True
    assert manual_player.is_playing is False
    assert response == ManualPlayerMessages.MANUAL_END
