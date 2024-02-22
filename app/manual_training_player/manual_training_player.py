import time
import json
import uuid

from app.manual_training_player.intents import ManualTrainingIntents

# Загрузка данных из JSON файла
with open('chapter_titles.json', 'r', encoding="utf-8") as f:
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
        self.human_readable_chapter_titles = (
            chapter_titles_data)['human_readable_chapter_titles']
        self.file_name_chapter_titles = (
            chapter_titles_data)['file_name_chapter_titles']

    def is_finished(self):
        self.is_finish = self.current_chapter is None and not self.greetings
        return self.is_finish

    def terminate_manual_training(self):
        if self.is_finished():
            return "Обучение уже завершено", {}
        else:
            self.is_finished()
            return "Обучение завершено", {}

    def process_request(self, command, intents):
        if not self.greetings:
            self.greetings = True
            return self.greet_user()
        elif ManualTrainingIntents.PAUSE_MANUAL_TRAINING in intents:
            return self.pause_playback()
        elif ManualTrainingIntents.RESUME_MANUAL_TRAINING in intents:
            return self.continue_playback()
        elif ManualTrainingIntents.NEXT_MANUAL_TRAINING_CHAPTER in intents:
            return self.play_next_chapter()
        elif ManualTrainingIntents.TERMINATE_MANUAL_TRAINING in intents:
            return self.is_finished()
        else:
            return self.process_learning_request(command, intents)

    def process_learning_request(self, command, intents):
        if not command:
            return self.unknown_command_response()
        elif ManualTrainingIntents.START_MANUAL_TRAINING in intents:
            self.current_chapter = 1
            return self.start_audio_playback(self.current_chapter)
        elif ManualTrainingIntents.SHOW_MANUAL_TRAINING_CONTENTS in intents:
            return self.get_table_of_contents()
        elif ManualTrainingIntents.GET_MANUAL_TRAINING_CHAPTER_INFO in intents:
            chapter_number = intents['get_manual_training_chapter_info']['slots']['chapter']['value']
            if chapter_number:
                try:
                    chapter_number = int(chapter_number)
                    chapter_name = self.get_chapter_name_by_number(chapter_number)
                    if chapter_name:
                        chapter_name_text = f"Название главы {chapter_number}: {chapter_name}"
                        return self.get_response(chapter_name_text)
                    else:
                        no_chapter_text = "Глава с указанным номером не найдена"
                        return self.get_response(no_chapter_text)
                except ValueError:
                    error_text = "Неверный формат номера главы"
                    return self.get_response(error_text)
            else:
                error_text = "Не указан номер главы"
                return self.get_response(error_text)
        elif ManualTrainingIntents.CHOOSE_MANUAL_TRAINING_CHAPTER in intents:
            chapter_number = intents['choose_manual_training_chapter']['slots']['chapter']['value']
            if str(chapter_number) in self.human_readable_chapter_titles:
                self.current_chapter = chapter_number
                return self.start_audio_playback(self.current_chapter)
            else:
                no_chapter_text = "Указанная глава не существует. Пожалуйста, выберите другую главу."
                return self.get_response(no_chapter_text)
        return self.unknown_command_response()

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
        audio_url = (
            f"https://www.guidedogs.acceleratorpracticum.ru/"
            f"{self.file_name_chapter_titles.get(str(chapter_number))}.mp3"
        )
        text = (
            f"Начинаю проигрывание главы номер {chapter_number} - "
            f"{self.human_readable_chapter_titles.get(str(chapter_number))}."
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
        toc = "Оглавление: "
        for chapter_num, title in self.human_readable_chapter_titles.items():
            toc += f"Глава {chapter_num} - {title}. "
        return toc, {}

    def get_response(self, text):
        return text, {}

    def select_chapter(self, chapter_number):
        self.current_chapter = chapter_number
        return self.start_audio_playback(self.current_chapter)

    def play_next_chapter(self):
        next_chapter_number = int(self.current_chapter) + 1
        if str(next_chapter_number) in self.human_readable_chapter_titles:
            self.current_chapter = str(next_chapter_number)
            return self.start_audio_playback(next_chapter_number)
        return self.get_response("Вы достигли конца книги.")

    def continue_playback(self):
        if self.current_chapter is not None:
            return self.start_audio_playback(self.current_chapter)
        error_text = "Нет текущей главы для продолжения."
        return self.get_response(error_text)

    def pause_playback(self):
        if self.is_playing:
            stop_time_ms = int(time.time() * 1000)
            elapsed_time_ms = stop_time_ms - self.audio_playback_start_time
            token = self.current_token
            if token in self.token_offsets:
                self.token_offsets[str(self.current_chapter)][
                    "offset_ms"
                ] += elapsed_time_ms
            else:
                self.token_offsets[self.current_chapter][
                    "offset_ms"
                ] = elapsed_time_ms
            self.is_playing = False
            text = "Остановила."
            directives = {"audio_player": {"action": "Stop"}}
            return text, directives
        return_text = "Проигрывание еще не началось."
        return self.get_response(return_text)

    def unknown_command_response(self):
        unknown_command_text = "Неизвестная команда."
        return self.get_response(unknown_command_text)

    def greet_user(self):
        with open('welcome_text.json', 'r', encoding="utf-8") as file:
            welcome_data = json.load(file)
        welcome_text = welcome_data['welcome_text']
        return self.get_response(welcome_text)

    def get_chapter_name_by_number(self, chapter_number):
        return self.human_readable_chapter_titles.get(str(chapter_number))


if __name__ == "__main__":
    from fastapi import FastAPI
    from app.main import RequestData
    app = FastAPI()

    audio_assistant = ManualTrainingPlayer()

#     # @app.post(
#     #     "/",
#     #     tags=["Alice project"],
#     #     summary="Диалог с Алисой.",
#     # )
#     # async def root(data: RequestData):
#     #     global audio_assistant
#     #     command = data.request.get("command")
#     #     response = audio_assistant.process_request(command)
#     #     return response
#
    print(audio_assistant.process_request("", {}))
    print(audio_assistant.process_request("", {}))
    print(audio_assistant.process_request("фамии", {}))
    print(audio_assistant.process_request("пауза", {"pause_manual_training"}))
    print(audio_assistant.process_request("3",
                                          {"choose_manual_training_chapter": {"slots": {"chapter": {"value": "3"}}}}))
    time.sleep(3)
    print(audio_assistant.process_request("пауза", {"pause_manual_training"}))
    print(audio_assistant.process_request("продолжить", {"resume_manual_training"}))
    print(audio_assistant.process_request("следующая", {"next_manual_training_chapter"}))
    print(audio_assistant.process_request("прослушать оглавление", {"show_manual_training_contents"}))
    print(audio_assistant.process_request("начинай", {"start_manual_training"}))
    print(audio_assistant.process_request("расскажи название главы", {"get_manual_training_chapter_info": {"slots": {"chapter": {"value": ""}}}}))
    print(audio_assistant.process_request("расскажи название главы 56", {"get_manual_training_chapter_info": {"slots": {"chapter": {"value": "56"}}}}))
    print(audio_assistant.process_request("Остановить обучение по методичке", {"terminate_manual_training"}))
