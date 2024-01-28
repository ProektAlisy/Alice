import json
import random
from typing import Final

from app.exceptions import (
    QuizFileNotFoundAliceException,
    QuizFileWrongFormatAliceException,
    QuizFileWrongAnswerAliceException,
    QuizIsFinishedAliceException,
    QuizNoActiveQuestionAliceException,
)

QUIZ_FILE_PATH = "app/quiz.json"


class QuizExceptionMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    QUIZ_FILE_WRONG_FORMAT: Final = "Ошибка формата в файле вопросов викторины"
    QUIZ_FILE_WRONG_ANSWER: Final = (
        "Неизвестный ответ <{answer}> в файле вопросов викторины для вопроса "
        "<{question}>"
    )
    QUIZ_IS_FINISHED: Final = (
        "Все вопросы викторины заданы. Викторина завершена!"
    )
    NO_ACTIVE_QUESTION_ERROR: Final = "Нет текущего вопроса для проверки!"


class QuizMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    CHOICE_FORMAT: Final = "{key} {value}"
    QUESTION_AND_CHOICES_FORMAT: Final = "{question}\n{choices}\n"
    FULL_QUESTION_FORMAT: Final = (
        "Вопрос {current_question_number}.\n"
        "{question_and_choices}\n"
        "Ваш вариант ответа"
    )
    CORRECT_ANSWER_FORMAT: Final = "Правильный ответ {choice} {answer}."
    RESULT_EXCELLENT: Final = "Превосходный результат! Вы ответили на все {total} вопросов без ошибок"
    RESULT_GOOD_1: Final = "Неплохой результат, всего одна ошибка"
    RESULT_GOOD_2: Final = "Неплохой результат, всего две ошибки"
    RESULT_NOT_BAD_3_4: Final = "Вы допустили {mistakes} ошибки. Не плохо, но думаю, стоит еще поучиться"
    RESULT_BAD: Final = "Вы допустили {mistakes} ошибок, это довольно много. Стоит еще поучиться"
    RESULT_VERY_BAD: Final = (
        "Вы допустили {mistakes} ошибок, это очень много. Стоит еще поучиться"
    )


class QuizQuestion:
    question: str
    choices: dict[str, str]
    correct_choice: str
    question_and_choices: str

    def __init__(self, data: dict):
        """Инициализация вопроса данными из словаря"""
        self.question = data.get("question")
        self.choices = data.get("choices")
        self.correct_choice = data.get("correct_choice")
        if (
            self.question is None
            or self.choices is None
            or self.correct_choice is None
        ):
            raise QuizFileWrongFormatAliceException(
                QuizExceptionMessages.QUIZ_FILE_WRONG_FORMAT
            )
        if self.correct_choice not in self.choices.keys():
            raise QuizFileWrongAnswerAliceException(
                QuizExceptionMessages.QUIZ_FILE_WRONG_ANSWER.format(
                    answer=self.correct_choice, question=self.question
                )
            )
        self.correct_choice = self.correct_choice.lower()
        # формирование отформатированной строки вопроса с ответами
        choices_as_str = "\n".join(
            [
                QuizMessages.CHOICE_FORMAT.format(
                    key=choice[0], value=choice[1]
                )
                for choice in self.choices.items()
            ]
        )
        self.question_and_choices = (
            QuizMessages.QUESTION_AND_CHOICES_FORMAT.format(
                question=self.question, choices=choices_as_str
            )
        )

    def __str__(self):
        return self.question_and_choices


class Quiz:
    questions: list[QuizQuestion] = []
    _correct_answers_count: int
    _current_question_number: int

    def __init__(self):
        self._questions = []
        self._correct_answers_count = 0
        self._current_question_number = 0

    @property
    def total_questions_count(self) -> int:
        return len(self._questions)

    @property
    def correct_answers_count(self) -> int:
        return self._correct_answers_count

    @property
    def current_question_number(self) -> int:
        return self._current_question_number + 1

    def load_questions(self, file_name: str):
        """Загрузка вопросов викторины из json файла.

        :param: file_name - наименование файла с вопросами следующего формата
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
        """
        try:
            with open(file_name, mode="r", encoding="utf-8") as in_file:
                self._questions = []
                questions_list = json.load(in_file)
                self._questions = [
                    QuizQuestion(record) for record in questions_list
                ]
        except FileNotFoundError as e:
            self._questions = []
            raise QuizFileNotFoundAliceException(e.filename)

    def restart(self, shuffle: bool = True):
        """Запуск викторины заново.

        :param: shuffle - перемешивать ли вопросы (True/False)
        """
        if shuffle:
            random.shuffle(self._questions)
        self._correct_answers_count = 0
        self._current_question_number = 0

    def is_finished(self) -> bool:
        """Завершена ли викторина."""
        return self._current_question_number >= self.total_questions_count

    def get_question(self) -> str:
        """Возвращает текущий вопрос и варианты ответов."""
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED
            )
        # если еще ни один из вопросов не задан, задаем первый
        return str(self._questions[self._current_question_number])

    def is_user_choice_correct(self, user_choice: str) -> bool:
        """Анализирует ответ пользователя на текущий вопрос."""
        if self.is_finished():
            raise QuizNoActiveQuestionAliceException(
                QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR
            )
        correct_choice = self._questions[
            self._current_question_number
        ].correct_choice
        return user_choice == correct_choice

    def get_current_answer(self) -> str:
        """Возвращает ответ на текущий вопрос в формате <буква ответ>"""
        if self.is_finished():
            raise QuizNoActiveQuestionAliceException(
                QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR
            )
        question = self._questions[self._current_question_number]
        answer = question.choices[question.correct_choice]
        return QuizMessages.CORRECT_ANSWER_FORMAT.format(
            choice=question.correct_choice, answer=answer
        )

    def advance_question(self, is_correct_answer: bool) -> str:
        """Обновляет количество верных ответов и обновляет номер текущего вопроса

        :param: is_correct_answer признак правильного ответа на текущий вопрос.
        """
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED
            )
        self._correct_answers_count += is_correct_answer
        self._current_question_number += 1


# -------------------------------
# quiz workflow example
# quiz = Quiz()
# quiz.load_questions(QUIZ_FILE_PATH)
# quiz.restart()
# while not quiz.is_finished():
#     question_and_choices = quiz.get_question()
#     print(
#         QuizMessages.FULL_QUESTION_FORMAT.format(
#             current_question_number=quiz._current_question_number + 1,
#             question_and_choices=question_and_choices,
#         )
#     )
#     answer = input()
#     is_correct_answer = quiz.is_user_choice_correct(answer)
#     if is_correct_answer:
#         print("Абсолютно верно!")
#     else:
#         print("К сожалению неверно!")
#         print(quiz.get_current_answer())
#     quiz.advance_question(is_correct_answer)
# print(
#     f"Результат викторины: {quiz.correct_answers_count} / {quiz.total_questions_count}",
# )
