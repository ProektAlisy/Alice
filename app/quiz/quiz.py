import json
import random

from app.constants.quiz.messages import QuizExceptionMessages, QuizMessages
from app.quiz.exceptions import (
    QuizFileNotFoundAliceException,
    QuizFileWrongAnswerAliceException,
    QuizFileWrongFormatAliceException,
    QuizIsFinishedAliceException,
    QuizNoActiveQuestionAliceException,
)


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
                    key=QuizQuestion.choice_to_tts(choice[0]),
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

    @classmethod
    def choice_to_tts(cls, choice: str) -> str:
        """Преобразует вариант ответа в tts.

        Добавляет "э" для б|в|г|д|ж|з

        Args:
            choice (str): Вариант ответа на вопрос (ключ)

        Returns:
            str: tts транскрипцию ответа.
        """
        if choice.lower() in "бвгджз":
            return choice + "э"
        return choice

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
            return
        self._mistakes_count = state.get("mistakes_count", 0)
        self._current_question_number = state.get("current_question_number", 0)
        order = state.get("questions_order", None)
        if order:
            self._questions_order = order

    def restart(self, shuffle: bool = True):
        """Запуск викторины заново.

        Args:
            shuffle: перемешивать ли вопросы.
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
