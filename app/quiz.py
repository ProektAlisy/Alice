import json
import random
from typing import Final

# from app.exceptions import FileNotFoundAliceException


class QuizMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    QUIZ_FILE_WRONG_FORMAT: Final = "Ошибка формата в файле вопросов викторины"
    QUIZ_FILE_WRONG_ANSWER: Final = (
        "Неизвестный ответ <{answer}> в файле вопросов викторины для вопроса "
        "<{question}>"
    )
    QUIZ_CHOICE_FORMAT: Final = "{key} {value}"
    QUIZ_QUESTION_FORMAT: Final = "{question}\n{choices}\n"
    QUIZ_FULL_QUESTION_FORMAT: Final = (
        "Вопрос {current_question_number}.\n"
        "{question_and_choices}\n"
        "Ваш вариант ответа"
    )
    QUIZ_IS_FINISHED: Final = (
        "Все вопросы викторины заданы. Викторина завершена!"
    )
    NO_ACTIVE_QUESTION_ERROR: Final = "Нет текущего вопроса для проверки!"
    CORRECT_ANSWER_FORMAT: Final = "Правильный ответ {choice} {answer}."


class AliceException(Exception):
    pass


class FileNotFoundAliceException(AliceException):
    pass


class QuizFileWrongFormatAliceException(AliceException):
    pass


class QuizFileWrongAnswerAliceException(AliceException):
    pass


class QuizIsFinishedAliceException(AliceException):
    pass


class QuizNoActiveQuestionAliceException(AliceException):
    pass


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
                QuizMessages.QUIZ_FILE_WRONG_FORMAT
            )
        if self.correct_choice not in self.choices.keys():
            raise QuizFileWrongAnswerAliceException(
                QuizMessages.QUIZ_FILE_WRONG_ANSWER.format(
                    answer=self.correct_choice, question=self.question
                )
            )
        self.correct_choice = self.correct_choice.lower()
        # формирование отформатированной строки вопроса с ответами
        choices_as_str = "\n".join(
            [
                QuizMessages.QUIZ_CHOICE_FORMAT.format(
                    key=choice[0], value=choice[1]
                )
                for choice in self.choices.items()
            ]
        )
        self.question_and_choices = QuizMessages.QUIZ_QUESTION_FORMAT.format(
            question=self.question, choices=choices_as_str
        )

    def __str__(self):
        return self.question_and_choices


class Quiz:
    questions: list[QuizQuestion] = []
    total_questions_count: int
    correct_answers_count: int
    current_question_number: int

    def __init__(self):
        self.questions = []
        self.total_questions_count = 0
        self.correct_answers_count = 0
        self.current_question_number = 0

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
                self.questions = []
                questions_list = json.load(in_file)
                self.questions = [
                    QuizQuestion(record) for record in questions_list
                ]
        except FileNotFoundError as e:
            self.questions = []
            raise FileNotFoundAliceException(e.filename)

    def restart(self):
        """Запуск викторины заново."""

        random.shuffle(self.questions)
        self.total_questions_count = len(self.questions)
        self.correct_answers_count = 0
        self.current_question_number = 0

    def is_finished(self) -> bool:
        """Завершена ли викторина."""

        return self.current_question_number > self.total_questions_count

    def get_question(self) -> str:
        """Возвращает текущий вопрос и варианты ответов."""
        if self.is_finished():
            raise QuizIsFinishedAliceException(QuizMessages.QUIZ_IS_FINISHED)
        # если еще ни один из вопросов не задан, задаем первый
        if self.current_question_number == 0:
            self.current_question_number = 1
        return str(self.questions[self.current_question_number - 1])

    def check_answer(self, user_choice: str) -> bool:
        """Анализирует ответ пользователя на текущий вопрос."""
        if 0 < self.current_question_number <= self.total_questions_count:
            correct_choice = self.questions[
                self.current_question_number - 1
            ].correct_choice
            return user_choice == correct_choice
        raise QuizNoActiveQuestionAliceException(
            QuizMessages.NO_ACTIVE_QUESTION_ERROR
        )

    def get_current_answer(self) -> str:
        """Возвращает ответ на текущий вопрос в формате <буква ответ>"""
        if 0 < self.current_question_number <= self.total_questions_count:
            question = self.questions[self.current_question_number - 1]
            answer = question.choices[question.correct_choice]
            return QuizMessages.CORRECT_ANSWER_FORMAT.format(
                choice=question.correct_choice, answer=answer
            )
        raise QuizNoActiveQuestionAliceException(
            QuizMessages.NO_ACTIVE_QUESTION_ERROR
        )


if __name__ == "__main__":
    quiz = Quiz()
    quiz.load_questions("app/quiz.json")
    quiz.restart()
    while not quiz.is_finished():
        question_and_choices = quiz.get_question()
        print(
            QuizMessages.QUIZ_FULL_QUESTION_FORMAT.format(
                current_question_number=quiz.current_question_number,
                question_and_choices=question_and_choices,
            )
        )
        answer = input()
        if quiz.check_answer(answer):
            print("Абсолютно верно!")
            quiz.correct_answers_count += 1
        else:
            print("К сожалению неверно!")
            print(quiz.get_current_answer())
        quiz.current_question_number += 1
    print(
        f"Результат викторины: {quiz.correct_answers_count} / {quiz.total_questions_count}",
    )
