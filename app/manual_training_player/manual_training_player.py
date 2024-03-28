import json
import time
import uuid

from app.constants.manual_training_player.intents import ManualTrainingIntents
from app.constants.manual_training_player.manual_training_messages import (
    ManualPlayerMessages,
)

CHAPTER_TITLES = "app/manual_training_player/chapter_titles.json"
WELCOME_TEXT = "app/manual_training_player/welcome_text.json"

# Загрузка данных из JSON файла
with open(
    CHAPTER_TITLES,
    "r",
    encoding="utf-8",
) as f:
    chapter_titles_data = json.load(f)


class ManualTrainingPlayer:
    def __init__(self):
        self.greetings = False
        self.current_token = None
        self.current_chapter = None
        self.is_playing = False
        self.audio_playback_start_time = 0
        self.token_offsets = {}
        self.is_finish = True
        self.human_readable_chapter_titles = (chapter_titles_data)[
            "human_readable_chapter_titles"
        ]
        self.file_name_chapter_titles = (chapter_titles_data)[
            "file_name_chapter_titles"
        ]
        self.final_audio_played = False

    def is_finished(self):
        return self.is_finish

    def terminate_manual_training(self):
        if self.is_finished():
            return ManualPlayerMessages.ALREADY_FINISHED, {}
        self.is_finish = True
        self.is_playing = False
        self.greetings = False
        self.token_offsets.clear()
        return ManualPlayerMessages.TRAINING_COMPLETED, {}

    def process_request(self, command, intents):
        if not self.greetings:
            self.greetings = True
            self.is_finish = False
            return self.greet_user()
        self.is_finish = False
        if ManualTrainingIntents.PAUSE_MANUAL_TRAINING in intents:
            return self.pause_playback()
        if ManualTrainingIntents.RESUME_MANUAL_TRAINING in intents:
            return self.continue_playback()
        if ManualTrainingIntents.NEXT_MANUAL_TRAINING_CHAPTER in intents:
            return self.play_next_chapter()
        if ManualTrainingIntents.TERMINATE_MANUAL_TRAINING in intents:
            return self.terminate_manual_training()
        return self.process_learning_request(command, intents)

    def process_learning_request(self, command, intents):
        if ManualTrainingIntents.START_MANUAL_TRAINING in intents:
            if not self.current_chapter:
                self.current_chapter = "1"
                return self.start_audio_playback(self.current_chapter)
            if self.is_playing:
                playback_text = ManualPlayerMessages.PLAYBACK_IS_ACTIVE
                return self.get_response(playback_text)
            return self.start_audio_playback(self.current_chapter)
        if ManualTrainingIntents.SHOW_MANUAL_TRAINING_CONTENTS in intents:
            return self.get_table_of_contents()
        if ManualTrainingIntents.GET_MANUAL_TRAINING_CHAPTER_INFO in intents:
            return self.get_chapter_name(intents)
        if ManualTrainingIntents.CHOOSE_MANUAL_TRAINING_CHAPTER in intents:
            return self.play_chapter_by_intent(intents)
        return self.unknown_command_response()

    def play_chapter_by_intent(self, intents):
        chapter_number = str(
            intents["choose_manual_training_chapter"]["slots"]["chapter"][
                "value"
            ],
        )
        if chapter_number in self.human_readable_chapter_titles:
            self.current_chapter = chapter_number
            return self.start_audio_playback(self.current_chapter)
        no_chapter_text = ManualPlayerMessages.NO_CHAPTER
        return self.get_response(no_chapter_text)

    def get_chapter_name(self, intents):
        chapter_number = intents["get_manual_training_chapter_info"]["slots"][
            "chapter"
        ]["value"]
        if chapter_number:
            try:
                chapter_number = int(chapter_number)
                chapter_name = self.get_chapter_name_by_number(chapter_number)
                if chapter_name:
                    if self.is_playing:
                        self._update_offset_ms()
                        self.is_playing = False
                        directives = {"audio_player": {"action": "Stop"}}
                        chapter_name_text = (
                            ManualPlayerMessages.CHAPTER_NAME.format(
                                chapter_number=chapter_number,
                                chapter_name=chapter_name,
                            )
                        )
                        return chapter_name_text, directives
                    chapter_name_text = (
                        ManualPlayerMessages.CHAPTER_NAME.format(
                            chapter_number=chapter_number,
                            chapter_name=chapter_name,
                        )
                    )
                    return self.get_response(chapter_name_text)
                no_chapter_text = ManualPlayerMessages.CHAPTER_NUMBER_NOT_FOUND
                return self.get_response(no_chapter_text)
            except ValueError:
                error_text = ManualPlayerMessages.INVALID_CHAPTER_NUMBER
                return self.get_response(error_text)
        error_text = ManualPlayerMessages.NO_CHAPTER_NUMBER
        return self.get_response(error_text)

    def start_audio_playback(self, chapter_number):
        token_info = self.token_offsets.get(chapter_number)
        if token_info is None:
            self.token_offsets.clear()
            token = str(uuid.uuid4())
            self.token_offsets[chapter_number] = {
                "token": token,
                "offset_ms": 0,
            }
            self.current_token = token
        else:
            self.current_token = token_info["token"]
        offset_ms = self.token_offsets[chapter_number]["offset_ms"]
        self.audio_playback_start_time = int(time.time() * 1000)
        self.is_playing = True
        audio_url = ManualPlayerMessages.CHAPTER_AUDIO_URL.format(
            chapter_name=self.file_name_chapter_titles.get(
                str(chapter_number),
            ),
        )
        text = ManualPlayerMessages.PLAYBACK_START.format(
            chapter_number=str(chapter_number),
            chapter_name=self.human_readable_chapter_titles.get(
                str(chapter_number),
            ),
        )
        directives = {
            "audio_player": {
                "action": "Play",
                "item": {
                    "stream": {
                        "url": audio_url,
                        "offset_ms": offset_ms,
                        "token": self.current_token,
                    },
                },
            },
        }
        return text, directives

    def get_table_of_contents(self):
        toc = self.get_all_chapters_text()
        if self.is_playing:
            self._update_offset_ms()
            self.is_playing = False
            directives = {"audio_player": {"action": "Stop"}}
            return toc + ManualPlayerMessages.CONTENT_END_PHRASE, directives
        return toc + ManualPlayerMessages.CONTENT_END_PHRASE, {}

    def get_all_chapters_text(self):
        toc = ManualPlayerMessages.CONTENT
        for chapter_num, title in self.human_readable_chapter_titles.items():
            toc += ManualPlayerMessages.CONTENT_CHAPTER.format(
                chapter_num=chapter_num,
                title=title,
            )
        return toc

    def get_response(self, text):
        return text, {}

    def select_chapter(self, chapter_number):
        self.current_chapter = chapter_number
        return self.start_audio_playback(self.current_chapter)

    def play_final_audio(self):
        if int(self.current_chapter) == 13:
            audio_url = ("https://www.guidedogs.acceleratorpracticum.ru/"
                         "finish.mp3")
            directives = {
                "audio_player": {
                    "action": "Play",
                    "item": {
                        "stream": {
                            "url": audio_url,
                            "token": str(uuid.uuid4()),
                        },
                    },
                },
            }
            self.current_chapter = None
            return ManualPlayerMessages.MANUAL_END, directives
        self.current_chapter = None
        return "", {}

    def play_next_chapter(self):
        next_chapter_number = str(int(self.current_chapter) + 1)
        if str(next_chapter_number) in self.human_readable_chapter_titles:
            self.current_chapter = str(next_chapter_number)
            return self.start_audio_playback(next_chapter_number)
        self.terminate_manual_training()
        return self.play_final_audio()

    def continue_playback(self):
        if self.current_chapter is not None:
            return self.start_audio_playback(self.current_chapter)
        error_text = ManualPlayerMessages.NO_CURRENT_CHAPTER
        return self.get_response(error_text)

    def pause_playback(self):
        if self.is_playing:
            self._update_offset_ms()
            self.is_playing = False
            text = ManualPlayerMessages.PLAYBACK_STOP
            directives = {"audio_player": {"action": "Stop"}}
            return text, directives
        return_text = ManualPlayerMessages.PLAYBACK_NOT_STARTED
        return self.get_response(return_text)

    def unknown_command_response(self):
        unknown_command_text = ManualPlayerMessages.UNKNOWN_COMMAND
        return self.get_response(unknown_command_text)

    def greet_user(self):
        with open(
            WELCOME_TEXT,
            "r",
            encoding="utf-8",
        ) as file:
            welcome_data = json.load(file)
        welcome_text = welcome_data["welcome_text"]
        return self.get_response(welcome_text)

    def get_chapter_name_by_number(self, chapter_number):
        return self.human_readable_chapter_titles.get(str(chapter_number))

    def _update_offset_ms(self):
        stop_time_ms = int(time.time() * 1000)
        elapsed_time_ms = stop_time_ms - self.audio_playback_start_time
        if self.current_chapter in self.token_offsets:
            self.token_offsets[self.current_chapter][
                "offset_ms"] += elapsed_time_ms
        else:
            self.token_offsets[self.current_chapter][
                "offset_ms"] = elapsed_time_ms

    def dump_state(self):
        """Возвращает словарь текущего состояния обучения.

        Returns:
            dict() - словарь текущего состояния вида::

            {
                "greetings": bool,
                "token": str | None,
                "chapter": str | None,
                "is_playing": bool,
                "audio_playback_start_time": str | None,
                "token_offsets": Dict | None,
                "is_finish": bool,
            }
        """
        return {
            "greetings": self.greetings,
            "token": self.current_token,
            "chapter": self.current_chapter,
            "is_playing": self.is_playing,
            "audio_playback_start_time": self.audio_playback_start_time,
            "token_offsets": self.token_offsets,
            "is_finish": self.is_finish,
        }

    def load_state(self, state: dict[str, str] | None):
        """Загружает информацию о состоянии обучения из словаря.

        Args:
            state - словарь сохраненного состояния вида::

            {
                "greetings": bool,
                "token": str | None,
                "chapter": str | None,
                "is_playing": bool,
                "audio_playback_start_time": str | None,
                "token_offsets": Dict | None,
                "is_finish": bool,
            }
        """
        if not state:
            self.greetings = False
            self.current_token = None
            self.current_chapter = None
            self.is_playing = False
            self.audio_playback_start_time = 0
            self.token_offsets = {}
            self.is_finish = True
            return
        self.greetings = state.get("greetings", False)
        self.current_token = state.get("token", None)
        self.current_chapter = state.get("chapter", None)
        self.is_playing = state.get("is_playing", False)
        self.audio_playback_start_time = state.get(
            "audio_playback_start_time", 0
        )
        self.token_offsets = state.get("token_offsets", None)
        self.is_finish = state.get("is_finish", True)
