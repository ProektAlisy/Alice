import json
import logging
import random
from enum import IntEnum
from typing import Final

from app.constants.quiz.intents import Intents
from app.exceptions import (
    QuizException,
    QuizFileNotFoundAliceException,
    QuizFileWrongAnswerAliceException,
    QuizFileWrongFormatAliceException,
    QuizIsFinishedAliceException,
    QuizNoActiveQuestionAliceException,
)

QUIZ_FILE_PATH = "app/quiz.json"


class QuizExceptionMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    QUIZ_FILE_WRONG_FORMAT: Final = "Ошибка формата в файле вопросов викторины"
    QUIZ_FILE_WRONG_ANSWER: Final = """
    Неизвестный ответ <{answer}> в файле вопросов викторины для вопроса
    <{question}>
    """
    QUIZ_IS_FINISHED: Final = (
        "Все вопросы викторины заданы. Викторина завершена!"
    )
    NO_ACTIVE_QUESTION_ERROR: Final = "Нет текущего вопроса для проверки!"


class QuizMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    CHOICE_FORMAT: Final = "{key}) sil <[300]> {value}. sil <[300]>"
    QUESTION_AND_CHOICES_FORMAT: Final = "{question}\n{choices}\n"
    FULL_QUESTION_FORMAT: Final = """
    Вопрос номер {current_question_number}.
    {question_and_choices}
    Ваш вариант ответа:
    """
    RULES: Final = """Вы оказались в разделе, где можете проверить насколько
        усвоен пройденный теоретический материал.
        Я задам Вам {total_questions_count} вопросов, и после каждого вопроса
        предложу три варианта ответа.
        Вам надо выбрать единственный правильный ответ.
        Для ответа просто назовите букву с правильным ответом: А, Б или В.
        Если чувствуете, что Вам пока не хватает знаний, скажите:
        'Завершить викторину'.
        Если нужно повторить вопрос и варианты ответов, скажите: 'Повтори'.
        Приступаем?
        """.replace(
        "\n",
        " ",
    )

    RULES_CHOICES: Final = """Если хотите начать викторину, скажите sil <[300]>
        'Приступаем', иначе скажите sil <[300]> 'Заверши викторину'.
        sil <[300]> Что вы решили, приступаем?
        """.replace(
        "\n",
        " ",
    )

    ALREADY_IN_PROGRESS: Final = """Вы вернулись. Как здорово!
        Напоминаю правила: Я задаю вопрос и
        предлагаю Вам на выбор три варианта ответа. Для ответа просто назовите
        букву с правильным ответом: А, Б или В. Правильный ответ может быть
        только один. У Вас есть незаконченная викторина. Сейчас вы остановились
        на вопросе номер {current_question_number}. Продолжим ее?
        Чтобы начать викторину заново скажите 'Начать заново'.
        """.replace(
        "\n",
        " ",
    )
    RESUME_REPEAT: Final = """Сейчас вы остановились на вопросе номер
    {current_question_number}.
        Чтобы продолжить викторину скажите 'Продолжим'.
        Чтобы начать викторину заново скажите 'Начать заново'.
        Чтобы завершить викторину скажите 'Завершить викторину'.
        """.replace(
        "\n",
        " ",
    )

    ALREADY_FINISHED: Final = "Викторина уже пройдена."
    RESET_PROGRESS: Final = """
    Чтобы начать викторину заново скажите 'Начать заново'.
    Это удалит весь предыдущий прогресс.
    """
    CHOICE_HELP: Final = """
    Чтобы ответить на вопрос назовите букву с правильным вариантом ответа
    А, sil <[200]> Б sil <[200]> или В.
    """
    CORRECT_ANSWER_FORMAT: Final = (
        "Правильный ответ '{choice}') sil <[200]> {answer}. sil <[500]>"
    )
    RESULT_EXCELLENT: Final = """
    Превосходный результат!
    Вы ответили на все {total} вопросов без ошибок.
    """
    RESULT_GOOD_1: Final = "Неплохой результат, всего одна ошибка."
    RESULT_GOOD_2: Final = "Неплохой результат, всего две ошибки."
    RESULT_NOT_BAD_3_4: Final = """
    Вы допустили {mistakes} ошибки.
    Не плохо, но думаю, стоит еще поучиться.
    """
    RESULT_BAD: Final = """Вы допустили {mistakes} ошибок, это довольно много.
        Стоит еще поучиться.
        """
    RESULT_VERY_BAD: Final = (
        "Вы допустили {mistakes} ошибок, это очень много. Стоит еще поучиться."
    )
    # форматы ответов при досрочном выходе
    PARTIAL_RESULT_0: Final = """
    Хорошо, завершаю викторину, но хочу сказать, что Вы отлично справились,
    не допустив ни одной ошибки.
    """
    PARTIAL_RESULT_1: Final = """
    Вы допустили всего одну ошибку. Не плохой результат.
    Завершаю викторину и жду Вашего возвращения.
    """
    PARTIAL_RESULT_NOT_BAD: Final = """
    Вы допустили {mistakes} ошибки. Не плохо, но думаю, стоит еще поучиться.
    Завершаю викторину и жду Вашего возвращения.
    """
    PARTIAL_RESULT_BAD: Final = """
    Вы допустили {mistakes} ошибок, это довольно много. Стоит еще поучиться.
    Завершаю викторину, но очень жду Вашего возвращения|
    """
    CORRECT_VARIANTS: Final = [
        "Поздравляю, это правильный ответ!",
        "Верно.",
        "Вы молодец.",
        "Потрясающе.",
        "Великолепно.",
    ]
    INCORRECT_VARIANTS: Final = [
        "К сожалению, нет.",
        "Ответ неверный.",
        "Не совсем так.",
    ]
    CHEER_UP_VARIANTS: Final = [
        """Не страшно, Вы здесь чтобы учиться.
        Попробуйте угадать ответ, а я Вам расскажу какой ответ правильный.
        """,
        """В теории мы это точно проходили, попробуйте вспомнить.
        Ничего страшного, если ошибетесь.
        """,
        "Давайте проверим вашу интуицию! Если не угадаете, я Вас поправлю.",
    ]
    NO_RESULTS: Final = """
    Завершаю викторину и жду Вашего возвращения sil <[200]>.
    """
    NO_QUIZ: Final = "Викторина временно недоступна!"
    UNKNOWN_COMMAND: Final = "Неизвестная команда!"
    AFTER_QUIZ: Final = "."


class QuizQuestion:
    question: str
    choices: dict[str, str]
    correct_choice: str
    question_and_choices: str

    def __init__(self, data: dict):
        """Инициализация вопроса данными из словаря.

        Args:
            data (dict["str, Any"]): вопрос с вариантами ответа вида::

            {
                "question": "Текст вопроса 1?",
                "choices": {
                    "а": "вариант ответа 1",
                    "б": "вариант ответа 2",
                    "в": "вариант ответа 3"
                },
                "correct_choice": "а|б|в"
            }

        Raises:
            QuizFileWrongFormatAliceException: если отсутствует любой из ключей
            QuizFileWrongAnswerAliceException: если значение "correct_choice"
            не содержится в списке ключей choices
        """
        self.question = data.get("question")
        self.choices = data.get("choices")
        self.correct_choice = data.get("correct_choice")
        if (
            self.question is None
            or self.choices is None
            or self.correct_choice is None
        ):
            raise QuizFileWrongFormatAliceException(
                QuizExceptionMessages.QUIZ_FILE_WRONG_FORMAT,
            )
        if self.correct_choice not in self.choices.keys():
            raise QuizFileWrongAnswerAliceException(
                QuizExceptionMessages.QUIZ_FILE_WRONG_ANSWER.format(
                    answer=self.correct_choice,
                    question=self.question,
                ),
            )
        self.correct_choice = self.correct_choice.lower()
        # формирование отформатированной строки вопроса с ответами
        choices_as_str = "\n".join(
            [
                QuizMessages.CHOICE_FORMAT.format(
                    key=choice[0],
                    value=choice[1],
                )
                for choice in self.choices.items()
            ],
        )
        self.question_and_choices = (
            QuizMessages.QUESTION_AND_CHOICES_FORMAT.format(
                question=self.question,
                choices=choices_as_str,
            )
        )

    def __str__(self):
        return self.question_and_choices


class Quiz:
    def __init__(self):
        self._questions = []
        self._mistakes_count = 0
        self._current_question_number = 0
        self._questions_order = []

    @property
    def total_questions_count(self) -> int:
        return len(self._questions)

    @property
    def mistakes_count(self) -> int:
        return self._mistakes_count

    @property
    def current_question_number(self) -> int:
        return self._current_question_number + 1

    def load_questions(self, file_name: str):
        """Загрузка вопросов викторины из json файла.

        Args:
            file_name (str): наименование файла вопросов следующего формата::

        [
            {
                "question": "Текст вопроса 1?",
                "choices": {
                    "а": "вариант ответа 1",
                    "б": "вариант ответа 2",
                    "в": "вариант ответа 3"
                },
                "correct_choice": "а|б|в"
            },
            ...
        ]
        Raises:
            QuizFileNotFoundAliceException: если файл file_name не найден
        """
        try:
            with open(file_name, mode="r", encoding="utf-8") as in_file:
                self._questions = []
                questions_list = json.load(in_file)
                self._questions = [
                    QuizQuestion(record) for record in questions_list
                ]
                self._questions_order = list(range(len(self._questions)))
        except FileNotFoundError as e:
            self._questions = []
            self._questions_order = []
            raise QuizFileNotFoundAliceException(e.filename)

    def dump_state(self) -> dict[str, str | int]:
        """Возвращает текущее состояние викторины в виде словаря.

        Returns:
            dict() - словарь вида::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int
            }
        """
        return {
            "questions_order": self._questions_order.copy(),
            "current_question_number": self._current_question_number,
            "mistakes_count": self._mistakes_count,
        }

    def load_state(self, state: dict[str, str] | None):
        """Загружает текущее состояние викторины из словаря.

        Args:
            state (dict): словарь состояния следующего формата::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int
            }
        """

        if not state:
            # self._mistakes_count = 0
            # self._current_question_number = 0
            # self._questions_order = list(range(len(self._questions)))
            return
        self._mistakes_count = state.get("mistakes_count", 0)
        self._current_question_number = state.get("current_question_number", 0)
        order = state.get("questions_order", None)
        if order:
            self._questions_order = order

    def restart(self, shuffle: bool = True):
        """Запуск викторины заново.

        Args:
            shuffle (bool): перемешивать ли вопросы (True/False)
        """
        if shuffle:
            random.shuffle(self._questions_order)
        self._mistakes_count = 0
        self._current_question_number = 0

    def _get_current_question(self) -> QuizQuestion:
        """Возвращает текущий вопрос викторины.

        Returns:
            QuizQuestion: текущий вопрос викторины

        Raises:
            QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR: если викторина
            завершена
        """
        if self.is_finished():
            raise QuizNoActiveQuestionAliceException(
                QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR,
            )
        return self._questions[
            self._questions_order[self._current_question_number]
        ]

    def is_finished(self) -> bool:
        """Завершена ли викторина."""
        return self._current_question_number >= self.total_questions_count

    def get_question(self) -> str:
        """Возвращает текущий вопрос и варианты ответов."""
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED,
            )
        # если викторина не завершена - возвращаем текст текущего вопроса
        return str(self._get_current_question())

    def is_user_choice_correct(self, user_choice: str) -> bool:
        """Анализирует ответ пользователя на текущий вопрос.

        Args:
            user_choice (str): ответ пользователя

        Returns:
            bool: True - если ответ соответствует правильному, False - иначе
        """
        correct_choice = self._get_current_question().correct_choice
        return user_choice == correct_choice

    def get_current_answer(self) -> str:
        """Возвращает ответ на текущий вопрос в формате <'БУКВА' ответ>"""
        question = self._get_current_question()
        answer = question.choices[question.correct_choice]
        return QuizMessages.CORRECT_ANSWER_FORMAT.format(
            choice=question.correct_choice.upper(),
            answer=answer,
        )

    def advance_question(self, is_correct_answer: bool) -> str:
        """Обновляет количество ошибочных ответов и номер текущего вопроса.

        Args:
            is_correct_answer (bool): правильность ответа на текущий вопрос.
        """
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED,
            )
        self._mistakes_count += not is_correct_answer
        self._current_question_number += 1


class QuizState(IntEnum):
    """Состояния диалога викторины."""

    INIT = 0
    RULES = 1
    IN_PROGRESS = 2
    FINISHED = 3
    TERMINATED = 4
    RESUME = 5


class QuizSkill:
    def __init__(self, filename: str = QUIZ_FILE_PATH):
        """Инициализация викторины вопросами из файла filename."""
        self._quiz = Quiz()
        self._state = QuizState.INIT
        try:
            self._quiz.load_questions(filename)
            self._quiz.restart()
        except QuizException as e:
            logging.exception(e)

    def is_finished(self) -> bool:
        """Возвращает True, если работа с викториной завершена.

        Returns:
            bool: True - если викторина не начата, или прервана досрочно или
            завершена и заданы все вопросы.
        """
        return self._state in (
            QuizState.INIT,
            QuizState.FINISHED,
            QuizState.TERMINATED,
        )

    def _get_final_result(self) -> str:
        """Возвращает строку результата для завершенной викторины."""
        match self._quiz.mistakes_count:
            case 0:
                return QuizMessages.RESULT_EXCELLENT.format(
                    self._quiz.current_question_number - 1,
                )
            case 1:
                return QuizMessages.RESULT_GOOD_1
            case 2:
                return QuizMessages.RESULT_GOOD_2
            case 3 | 4:
                return QuizMessages.RESULT_NOT_BAD_3_4.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case 5 | 6:
                return QuizMessages.RESULT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case _:
                return QuizMessages.RESULT_VERY_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
        return ""

    def _get_partial_result(self) -> str:
        """Возвращает строку промежуточного результата прерванной викторины."""
        match self._quiz.mistakes_count:
            case 0:
                return QuizMessages.PARTIAL_RESULT_0
            case 1:
                return QuizMessages.PARTIAL_RESULT_1
            case 2 | 3 | 4:
                return QuizMessages.PARTIAL_RESULT_NOT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case _:
                return QuizMessages.PARTIAL_RESULT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
        return ""

    def _get_current_result(self) -> str:
        """Возвращает строку текущего результата викторины."""
        if self._quiz.is_finished():
            return self._get_final_result() + QuizMessages.AFTER_QUIZ
        return self._get_partial_result() + QuizMessages.AFTER_QUIZ

    def _get_full_question(self) -> str:
        """Возвращает полный текст вопроса с вариантами ответов."""
        question_and_choices = self._quiz.get_question()
        return QuizMessages.FULL_QUESTION_FORMAT.format(
            current_question_number=self._quiz.current_question_number,
            question_and_choices=question_and_choices,
        )

    def _get_answer_result(self, is_correct_answer: bool) -> str:
        """Возвращает результат в зависимости от правильности ответа."""
        if is_correct_answer:
            return random.choice(QuizMessages.CORRECT_VARIANTS)
        return (
            random.choice(QuizMessages.INCORRECT_VARIANTS)
            + self._quiz.get_current_answer()
        )

    def dump_state(self):
        """Возвращает словарь текущего состояния.

        Returns:
            dict() - словарь текущего состояния вида::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int,
                "state": int
            }
        """
        state = self._quiz.dump_state()
        state["state"] = int(self._state)
        return state

    def load_state(self, state: dict[str, str] | None):
        """Загружает информацию о состоянии викторины из словаря.

        Args:
            state - словарь сохраненного состояния вида::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int,
                "state": int
            }
        """
        if not state:
            self._quiz.load_state(None)
            self._state = QuizState.INIT
            return
        state_tmp = state.copy()
        if "state" in state_tmp:
            self._state = QuizState(state_tmp.pop("state"))
        self._quiz.load_state(state_tmp)

    def _process_init_state(
        self,
        *args,
    ) -> tuple[bool, str]:
        """Обработчик начального запуска до показа правил."""
        self._state = QuizState.RULES
        return True, QuizMessages.RULES.format(
            total_questions_count=self._quiz.total_questions_count,
        )

    def _process_rules_state(
        self,
        intents: dict[str],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик первоначального показа правил."""
        if Intents.TAKE_QUIZ in intents or Intents.REPEAT in intents:
            # повторить правила
            return True, QuizMessages.RULES.format(
                total_questions_count=self._quiz.total_questions_count,
            )
        if Intents.TERMINATE_QUIZ in intents:
            # выход до показа первого вопроса
            self._state = QuizState.INIT
            return True, QuizMessages.NO_RESULTS + QuizMessages.AFTER_QUIZ
        if Intents.AGREE in intents:
            # получено согласие на запуск викторины
            self._state = QuizState.IN_PROGRESS
            if not self._quiz.is_finished():
                return True, self._get_full_question()
            return True, QuizMessages.NO_QUIZ
        # return False, QuizMessages.UNKNOWN_COMMAND
        # при нераспознанной команде подсказка для выбора
        return True, QuizMessages.RULES_CHOICES

    def _process_in_progress_state(
        self,
        intents: dict[str],
        command: str,
    ) -> tuple[bool, str]:
        """Обработчик в режиме прогресса викторины."""
        if Intents.REPEAT in intents:
            # повторить последний вопрос
            return True, self._get_full_question()
        if Intents.NO_ANSWER in intents:
            # нет ответа - подбодрить
            return True, random.choice(QuizMessages.CHEER_UP_VARIANTS)
        if Intents.TERMINATE_QUIZ in intents:
            # досрочно завершить викторину
            self._state = QuizState.TERMINATED
            return True, self._get_current_result()
        if command in "абв":
            # обработка ответа
            is_correct_answer = self._quiz.is_user_choice_correct(command)
            answer_result = self._get_answer_result(is_correct_answer)
            self._quiz.advance_question(is_correct_answer)
            if self._quiz.is_finished():
                self._state = QuizState.FINISHED
                answer_result += self._get_current_result()
            else:
                answer_result += self._get_full_question()
            return True, answer_result
        # неизвестный вариант ответа - показать подсказку
        return True, QuizMessages.CHOICE_HELP

    def _process_finished_state(
        self,
        intents: dict[str],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик в режиме завершенной викторины."""
        if Intents.TAKE_QUIZ in intents:
            # викторина уже завершена
            result = " ".join(
                [
                    QuizMessages.ALREADY_FINISHED,
                    self._get_final_result(),
                    QuizMessages.RESET_PROGRESS,
                ],
            )
            return True, result
        if Intents.START_AGAIN in intents:
            # запустить заново
            self._state = QuizState.RULES
            self._quiz.restart()
            return True, QuizMessages.RULES.format(
                total_questions_count=self._quiz.total_questions_count,
            )
        return False, QuizMessages.UNKNOWN_COMMAND

    def _process_terminated_state(
        self,
        intents: dict[str],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик досрочно завершенной викторины."""
        if Intents.TAKE_QUIZ in intents:
            # викторина уже завершена
            self._state = QuizState.RESUME
            return True, QuizMessages.ALREADY_IN_PROGRESS.format(
                current_question_number=self._quiz.current_question_number,
            )
        return False, ""

    def _process_resume_state(
        self,
        intents: dict[str],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик диалога возобновления викторины."""
        if Intents.REPEAT in intents:
            # повторить диалог возобновления викторины
            return True, QuizMessages.RESUME_REPEAT.format(
                current_question_number=self._quiz.current_question_number,
            )
        if Intents.START_AGAIN in intents:
            # запустить заново
            self._quiz.restart()
            self._state = QuizState.IN_PROGRESS
            return True, self._get_full_question()
        if Intents.CONTINUE in intents:
            # продолжить
            self._state = QuizState.IN_PROGRESS
            return True, self._get_full_question()
        if Intents.TERMINATE_QUIZ in intents:
            # досрочно завершить викторину
            self._state = QuizState.TERMINATED
            return True, self._get_current_result()
        # повторить диалог возобновления викторины
        return True, QuizMessages.RESUME_REPEAT.format(
            current_question_number=self._quiz.current_question_number,
        )

    def execute_command(
        self,
        command: str,
        intents: dict[str],
    ) -> tuple[bool, str]:
        """Анализ и исполнение команды/интента.

        Args:
            command (str): Команда для навыка.
            intents (dict[str]): Словарь намерений (intents) для навыка.

        Returns:
            (result, answer): Кортеж ответа, где.
            result (bool): True, если команда воспринята викториной.
            answer (str): Текстовое сообщение ответа на команду.
        """
        command = command.lower()
        state_processors = {
            QuizState.INIT: self._process_init_state,
            QuizState.RULES: self._process_rules_state,
            QuizState.IN_PROGRESS: self._process_in_progress_state,
            QuizState.FINISHED: self._process_finished_state,
            QuizState.TERMINATED: self._process_terminated_state,
            QuizState.RESUME: self._process_resume_state,
        }
        if self._state in state_processors:
            return state_processors[self._state](intents, command)
        return False, ""
