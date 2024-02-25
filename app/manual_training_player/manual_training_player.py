import json
import time
import uuid

from app.constants.manual_training_player.intents import ManualTrainingIntents
from app.constants.manual_training_player.manual_training_player_messages import (
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

    def is_finished(self):
        return self.is_finish

    def terminate_manual_training(self):
        if self.is_finished():
            return ManualPlayerMessages.ALREADY_FINISHED, {}
        self.is_finish = True
        self.greetings = False
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
            elif self.is_playing:
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
        else:
            error_text = ManualPlayerMessages.NO_CHAPTER_NUMBER
            return self.get_response(error_text)

    def start_audio_playback(self, chapter_number):
        token_info = self.token_offsets.get(chapter_number)
        if token_info is None:
            token = str(uuid.uuid4())
            self.token_offsets[chapter_number] = {
                "token": token,
                "offset_ms": 0,
            }
        else:
            token = token_info["token"]
        self.current_token = token
        offset_ms = self.token_offsets[chapter_number]["offset_ms"]
        self.audio_playback_start_time = int(time.time() * 1000)
        self.is_playing = True
        audio_url = ManualPlayerMessages.AUDIO_URL.format(
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
        toc = ManualPlayerMessages.CONTENT
        for chapter_num, title in self.human_readable_chapter_titles.items():
            toc += ManualPlayerMessages.CONTENT_CHAPTER.format(
                chapter_num=chapter_num,
                title=title,
            )
        return toc, {}

    def get_response(self, text):
        return text, {}

    def select_chapter(self, chapter_number):
        self.current_chapter = chapter_number
        return self.start_audio_playback(self.current_chapter)

    def play_next_chapter(self):
        next_chapter_number = str(int(self.current_chapter) + 1)
        if str(next_chapter_number) in self.human_readable_chapter_titles:
            self.current_chapter = str(next_chapter_number)
            return self.start_audio_playback(next_chapter_number)
        return self.get_response(ManualPlayerMessages.MANUAL_END)

    def continue_playback(self):
        if self.current_chapter is not None:
            return self.start_audio_playback(self.current_chapter)
        error_text = ManualPlayerMessages.NO_CURRENT_CHAPTER
        return self.get_response(error_text)

    def pause_playback(self):
        if self.is_playing:
            stop_time_ms = int(time.time() * 1000)
            elapsed_time_ms = stop_time_ms - self.audio_playback_start_time
            token = self.current_token
            if token in self.token_offsets[self.current_chapter]["token"]:
                self.token_offsets[self.current_chapter][
                    "offset_ms"
                ] += elapsed_time_ms
            else:
                self.token_offsets[self.current_chapter][
                    "offset_ms"
                ] = elapsed_time_ms
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