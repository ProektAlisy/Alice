import json
import logging
import random
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
        "Вопрос номер {current_question_number}.\n"
        "{question_and_choices}\n"
        "Ваш вариант ответа:"
    )
    RULES: Final = (
        "Вы оказались в разделе, где можете проверить насколько усвоен"
        " пройденный теоретический материал. Я задам Вам {total_questions_count} вопросов,"
        " после каждого вопроса, и предложу три варианта ответа."
        " Вам надо выбрать единственный правильный ответ."
        " Для ответа просто назовите букву с правильным ответом: А, Б или В."
        " Если нужно повторить вопрос и варианты ответов, скажите: 'Повтори'."
        " Приступаем?"
    )
    ALREADY_IN_PROGRESS: Final = (
        "Вы оказались в разделе, где можете проверить насколько усвоен"
        " пройденный теоретический материал."
        " После каждого вопроса, и предложу три варианта ответа."
        " Вам надо выбрать единственный правильный ответ."
        " Для ответа просто назовите букву с правильным ответом: А, Б или В."
        " Если нужно повторить вопрос и варианты ответов, скажите: 'Повтори'."
        " Сейчас вы остановились на вопросе номер {current_question_number}."
    )
    ALREADY_FINISHED: Final = "Викторина уже пройдена."
    RESET_PROGRESS: Final = (
        "Чтобы начать викторину заново скажите 'Начать заново'."
        " Это удалит весь предыдущий прогресс."
    )
    CHOICE_HELP: Final = "Чтобы ответить на вопрос назовите букву с правильным вариантом ответа - А, Б или В"
    CORRECT_ANSWER_FORMAT: Final = "Правильный ответ '{choice}' {answer}."
    RESULT_EXCELLENT: Final = "Превосходный результат! Вы ответили на все {total} вопросов без ошибок"
    RESULT_GOOD_1: Final = "Неплохой результат, всего одна ошибка"
    RESULT_GOOD_2: Final = "Неплохой результат, всего две ошибки"
    RESULT_NOT_BAD_3_4: Final = "Вы допустили {mistakes} ошибки. Не плохо, но думаю, стоит еще поучиться"
    RESULT_BAD: Final = "Вы допустили {mistakes} ошибок, это довольно много. Стоит еще поучиться"
    RESULT_VERY_BAD: Final = (
        "Вы допустили {mistakes} ошибок, это очень много. Стоит еще поучиться"
    )
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
        (
            "Не страшно, Вы здесь чтобы учиться. "
            "Попробуйте угадать ответ, а я Вам расскажу какой ответ правильный."
        ),
        (
            "В теории мы это точно проходили, попробуйте вспомнить. "
            "Ничего страшного, если ошибетесь."
        ),
        ("Давайте проверим вашу интуицию! Если не угадаете, я Вас поправлю."),
    ]


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
        self._mistakes_count = 0
        self._current_question_number = 0

    def is_finished(self) -> bool:
        """Завершена ли викторина."""
        return self._current_question_number >= self.total_questions_count

    def get_question(self) -> str:
        """Возвращает текущий вопрос и варианты ответов."""
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED,
            )
        # если еще ни один из вопросов не задан, задаем первый
        return str(self._questions[self._current_question_number])

    def is_user_choice_correct(self, user_choice: str) -> bool:
        """Анализирует ответ пользователя на текущий вопрос."""
        if self.is_finished():
            raise QuizNoActiveQuestionAliceException(
                QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR,
            )
        correct_choice = self._questions[
            self._current_question_number
        ].correct_choice
        return user_choice == correct_choice

    def get_current_answer(self) -> str:
        """Возвращает ответ на текущий вопрос в формате <'БУКВА' ответ>"""
        if self.is_finished():
            raise QuizNoActiveQuestionAliceException(
                QuizExceptionMessages.NO_ACTIVE_QUESTION_ERROR,
            )
        question = self._questions[self._current_question_number]
        answer = question.choices[question.correct_choice]
        return QuizMessages.CORRECT_ANSWER_FORMAT.format(
            choice=question.correct_choice.upper(),
            answer=answer,
        )

    def advance_question(self, is_correct_answer: bool) -> str:
        """Обновляет количество ошибочных ответов и обновляет номер текущего вопроса

        :param: is_correct_answer признак правильного ответа на текущий вопрос.
        """
        if self.is_finished():
            raise QuizIsFinishedAliceException(
                QuizExceptionMessages.QUIZ_IS_FINISHED,
            )
        self._mistakes_count += not is_correct_answer
        self._current_question_number += 1


class QuizSkill:
    def __init__(self):
        self._quiz = Quiz()
        self._in_progress = False
        try:
            self._quiz.load_questions(QUIZ_FILE_PATH)
            self._quiz.restart()
        except QuizException as e:
            logging.exception(e)
            # raise e

    def _get_current_result(self) -> str:
        """Возвращает текстовую строку согласно текущему результату."""

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
        else:
            return (
                random.choice(QuizMessages.INCORRECT_VARIANTS)
                + " "
                + self._quiz.get_current_answer()
            )

    def execute_command(
        self,
        command: str,
        intents: dict[str],
    ) -> tuple[bool, str]:
        """Анализ и исполнение команды/интента.

        :param: command - команда для навыка
        :param: intents - словарь намерений (intents) для навыка

        :returns: (result, answer)
        result: bool - True, если команда воспринята викториной
        answer: str - текстовое сообщение ответа на команду
        """
        command = command.lower()
        if not self._in_progress and (
            Intents.TAKE_QUIZ in intents or Intents.REPEAT in intents
        ):
            # первый вход, показываем правила
            return True, QuizMessages.RULES.format(
                total_questions_count=self._quiz.total_questions_count,
            )
        elif self._in_progress and Intents.TAKE_QUIZ in intents:
            if not self._quiz.is_finished():
                return True, QuizMessages.ALREADY_IN_PROGRESS.format(
                    current_question_number=self._quiz.current_question_number,
                )
            # викторина уже завершена
            result = " ".join(
                [
                    QuizMessages.ALREADY_FINISHED,
                    self._get_current_result(),
                    QuizMessages.RESET_PROGRESS,
                ],
            )
            return True, result
        if (
            self._in_progress
            and self._quiz.is_finished()
            and Intents.START_AGAIN in intents
        ):
            # запустить заново
            self._quiz.restart()
            return True, self._get_full_question()
        if self._in_progress and Intents.REPEAT in intents:
            # повторить
            if self._quiz.is_finished():
                return True, self._get_current_result()
            else:
                return True, self._get_full_question()
        if not self._in_progress and Intents.AGREE in intents:
            # получено согласие на запуск викторины
            self._in_progress = True
            if not self._quiz.is_finished():
                return True, self._get_full_question()
            return True, "Викторина пока недоступна!!!"
        if self._in_progress and not self._quiz.is_finished():
            if Intents.NO_ANSWER in intents:
                return True, random.choice(QuizMessages.CHEER_UP_VARIANTS)
            if command not in "абв":
                return True, QuizMessages.CHOICE_HELP
            is_correct_answer = self._quiz.is_user_choice_correct(command)
            answer_result = self._get_answer_result(is_correct_answer)
            self._quiz.advance_question(is_correct_answer)
            if self._quiz.is_finished():
                answer_result += "\n" + self._get_current_result()
            else:
                answer_result += "\n" + self._get_full_question()
            return True, answer_result
        return False, ""
