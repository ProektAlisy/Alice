import time
import uuid


class AudioAssistant:
    def __init__(self):
        self.greetings = False
        self.current_token = None
        self.current_chapter = None
        self.is_playing = False
        self.audio_playback_start_time = 0
        self.token_offsets = {}
        self.is_finish = True
        self.human_readable_chapter_titles = {
            0: "Вступление",
            1: "Часто задаваемые вопросы",
            2: "Общий курс дрессировки",
            3: "Специальный курс дрессировки",
            4: "Типичные ошибки при работе с собакой - поводырем",
            5: "Работа на месте и изучение новых маршрутов",
            6: "Ориентировка с собакой",
            7: "Кормление собаки - поводыря",
            8: "Содержание собаки - поводыря",
            9: "Профилактика заболеваний собаки - поводыря",
            10: "Техника безопасности",
            11: "Снаряжение собаки - поводыря",
            12: "Контактная информация",
        }
        self.file_name_chapter_titles = {
            0: "00-vstuplenie",
            1: "01-chasto-zadavaemye-voprosy",
            2: "02-obshchij-kurs-dressirovki",
            3: "03-specialnyj-kurs-dressirovki",
            4: "04-tipichnye-oshibki-pri-rabote-s-sobakoj-povodyrem",
            5: "05-rabota-na-meste-i-izuchenie-novyh-marshrutov",
            6: "06-orientirovka-s-sobakoj",
            7: "07-kormlenie-sobaki-povodyrya",
            8: "08-soderzhanie-sobaki-povodyrya",
            9: "09-profilaktika-zabolevanij-sobaki-povodyrya",
            10: "10-tekhnika-bezopasnosti",
            11: "11-snaryazhenie-sobaki-povodyrya",
            12: "12-kontaktnaya-informaciya",
        }

    def is_finished(self):
        # TODO реализовать функцию после обработки команды "выход",
        #  "завершить обучение"
        self.is_finish = self.current_chapter is None and not self.greetings
        return self.is_finish

    def process_request(self, command, intents):
        # TODO добавить обработку интентов
        if not self.greetings:
            self.greetings = True
            return self.greet_user()
        if command == "пауза":
            return self.pause_playback()
        if command == "продолжить":
            return self.continue_playback()
        if command == "следующая":
            return self.play_next_chapter()
        return self.process_learning_request(command, intents)

    def process_learning_request(self, command, intents):
        # TODO добавить обработку интентов
        if not command:
            return self.unknown_command_response()
        if command == "начинай":
            self.current_chapter = 0
            return self.start_audio_playback(self.current_chapter)
        if command == "прослушать оглавление":
            return self.get_table_of_contents()
        if command == "выбрать главу":
            text = "Какую главу хотите прослушать?"
            return self.get_response(text)
        if (
            command.isdigit()
            and int(command) in self.human_readable_chapter_titles
        ):
            self.current_chapter = int(command)
            return self.start_audio_playback(self.current_chapter)
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
            f"{self.file_name_chapter_titles[chapter_number]}.mp3"
        )
        text = (
            f"Начинаю проигрывание главы "
            f"{self.human_readable_chapter_titles[chapter_number]}"
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
        toc = "Оглавление:"
        for chapter_num, title in self.human_readable_chapter_titles.items():
            toc += f"Глава {chapter_num} - {title}."
        return toc, {}

    def get_response(self, text):
        # response with no directives
        return text, {}

    def select_chapter(self, chapter_number):
        self.current_chapter = chapter_number
        return self.start_audio_playback(self.current_chapter)

    def play_next_chapter(self):
        # если главы начинаются с 1, то 'is not None' лишнее !
        if self.current_chapter is not None:
            next_chapter_number = self.current_chapter + 1
            if next_chapter_number in self.human_readable_chapter_titles:
                self.current_chapter = next_chapter_number
                return self.start_audio_playback(next_chapter_number)
            return self.get_response("Вы достигли конца книги.")
        return self.get_response("Не выбрана текущая глава.")

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
                self.token_offsets[self.current_chapter][
                    "offset_ms"
                ] += elapsed_time_ms
            else:
                self.token_offsets[self.current_chapter][
                    "offset_ms"
                ] = elapsed_time_ms
            self.is_playing = False
            text = "Пауза проигрывания."
            directives = {"audio_player": {"action": "Stop"}}
            return text, directives
        return_text = "Проигрывание еще не началось."
        return self.get_response(return_text)

    def unknown_command_response(self):
        unknown_command_text = "Неизвестная команда."
        return self.get_response(unknown_command_text)

    def greet_user(self):
        welcome_text = (
            "В 2018 году мы издали “Методическое пособие для владельцев и"
            "будущих владельцев собак-проводников”. "
            "У меня есть аудиоверсия этого пособия. Здесь Вы можете прослушать"
            "главы по выбору или по порядку. "
            "Воспроизведение можно ставить на паузу, а так же можно сказать"
            "'следующая глава' для того чтобы"
            "пропустить какую-нибудь тему. Для прослушивания списка всех тем"
            "скажите 'Оглавление' и после Вы "
            "сможете выбрать главу или скажите 'Начинай' и я начну"
            "воспроизведение методички по порядку."
        )
        return self.get_response(welcome_text)


# if __name__ == "__main__":
#     from fastapi import FastAPI
#     from pydantic import BaseModel
#
#     app = FastAPI()
#
#     audio_assistant = AudioAssistant()

# @app.post(
#     "/",
#     tags=["Alice project"],
#     summary="Диалог с Алисой.",
# )
# async def root(data: RequestData):
#     global audio_assistant
#     command = data.request.get("command")
#     response = audio_assistant.process_request(command)
#     return response

# print(audio_assistant.process_request(""))
# print(audio_assistant.process_request("3"))
# time.sleep(3)
# print(audio_assistant.process_request("пауза"))
# print(audio_assistant.process_request("продолжить"))
# print(audio_assistant.process_request("следующая"))
# print(audio_assistant.process_request("прослушать оглавление"))
# print(audio_assistant.process_request("начинай"))
