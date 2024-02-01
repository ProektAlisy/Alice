import logging

from transitions import Machine

from app.constants.answers import Answers
from app.constants.commands_triggers_functions import GetFunc
from app.constants.states import TRANSITIONS
from app.utils import (
    get_func_answers_command,
    get_trigger_by_command,
    get_triggers_by_order,
)
from app.quiz import QuizSkill

logging.basicConfig(level=logging.INFO)

QUIZ_SESSION_STATE_KEY = "quiz_state"


class FiniteStateMachine(object):
    states = [
        "start",
        "help",
        "discounts_free_services",
        "training",
        "quiz",
        "legislation",
        "services_for_blind",
    ]

    def __init__(self):
        self.message = ""
        self.saved_state = None
        self.progress = None
        self.incorrect_answers = 0
        self.machine = Machine(
            model=self,
            states=FiniteStateMachine.states,
            transitions=TRANSITIONS,
            initial="start",
        )
        self.max_progress = len(get_triggers_by_order())
        self.create_functions()
        self.quiz_skill = QuizSkill()

    def _save_state(self):
        self.saved_state = self.state

    def _save_progress(self, step: str) -> None:
        """Прогресс прохождения навыка."""
        if self.progress is None:
            self.progress = []
        if step not in self.progress:
            self.progress.append(step)
        else:
            self.progress.remove(step)
            self.progress.append(step)

    def _return_to_original_state(self):
        self.machine.set_state(self.saved_state)

    def get_help(self):
        self.saved_state = self.state
        self.message = Answers.HELP_MAIN

    def get_help_phrase(self):
        self.message = Answers.HELP_PHRASE

    def get_help_navigation(self):
        self.message = Answers.HELP_NAVIGATION

    def get_help_exit(self):
        self.message = Answers.EXIT_FROM_HELP

    def get_exit(self):
        self.message = Answers.EXIT_FROM_SKILL

    def generate_function(self, name, message, command):
        def func():
            self.message = message
            if name in GetFunc.NOT_CORE_COMMANDS:
                self._save_state()
            self._save_progress(get_trigger_by_command(command))

        setattr(self, name, func)

    def create_functions(self):
        [
            self.generate_function(func_name, answer, command)
            for func_name, answer, command in get_func_answers_command()
        ]

    def dont_understand(self):
        """
        Метод для обработки ответов, когда система не понимает пользователя.
        Увеличивает счетчик ответов и устанавливает сообщение
        в зависимости от счетчика.
        """
        self.incorrect_answers += 1
        if self.incorrect_answers <= 1:
            self.message = Answers.DONT_UNDERSTAND_THE_FIRST_TIME
        elif self.incorrect_answers == 2:
            self.message = Answers.DONT_UNDERSTAND_THE_SECOND_TIME
        else:
            self.message = Answers.DONT_UNDERSTAND_MORE_THAN_TWICE
        return self.message

    def dump_session_state(self) -> dict:
        """Функция возвращает словарь ответа для сохранения состояния навыка.

        Returns:
            dict(): словарь сохраненного состояния вида::

            {
                "quiz_state": { .... } - параметры состояния викторины
                ...
            }
        """

        state = {QUIZ_SESSION_STATE_KEY: self.quiz_skill.dump_state()}
        # state["test_value"] = 123
        # тут добавляем другие ключи для других разделов,
        # если нужно что-то хранить, например текущее состояние
        return state

    def load_session_state(self, session_state: dict):
        """Функция загружает текущее состояние из словаря session_state."""
        quiz_state = None
        if QUIZ_SESSION_STATE_KEY in session_state:
            quiz_state = session_state.pop(QUIZ_SESSION_STATE_KEY)
        self.quiz_skill.load_state(quiz_state)
        # тут возможна загрузка других ключей при необходимости
