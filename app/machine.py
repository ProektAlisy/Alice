import logging

from transitions import Machine

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
)

from app.constants.commands import ServiceCommands
from app.constants.skill_transitions import TRANSITIONS
from app.constants.states import STATES
from app.utils import get_func_answers_command, get_trigger_by_command
from app.quiz import QuizSkill

QUIZ_SESSION_STATE_KEY = "quiz_state"

logging.basicConfig(level=logging.INFO)

class FiniteStateMachine(object):
    states = STATES

    def __init__(self):
        self.message = ""
        self.saved_state = None
        self.progress = None
        self.incorrect_answers = 0
        self.command = ""
        self.machine = Machine(
            model=self,
            states=FiniteStateMachine.states,
            transitions=TRANSITIONS,
            initial="start",
        )
        self.flag = False
        self.max_progress = len(self.states)
        self.create_agree_functions()
        self.create_disagree_functions()
        self.quiz_skill = QuizSkill()

    def _save_progress(self, step: str, command: str) -> None:
        """Прогресс прохождения навыка."""
        if self.progress is None:
            self.progress = []
        if self.flag:
            self.progress = list(set(self.progress) - {step}) + [step]

    def generate_function(self, name, message, command):
        def func():
            self.message = message
            self._save_progress(
                get_trigger_by_command(
                    command,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                ),
                command,
            )

        setattr(self, name, func)

    def create_agree_functions(self):
        [
            self.generate_function(
                func_name,
                answer + " " + after_answer,
                command,
            )
            for func_name, answer, after_answer, _, command in get_func_answers_command(  # noqa
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        ]

    def create_disagree_functions(self) -> None:
        """Создание функций, обрабатывающих отказы пользователя.

        Args:
            self: Объект FiniteStateMachine.
        """
        [
            self.generate_function(
                func_name + "_disagree",
                disagree_answer,
                command,
            )
            for func_name, _, _, disagree_answer, command in get_func_answers_command(  # noqa
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        ]

    def dont_understand(self) -> str:
        """Обработка ответов, когда система не понимает пользователя.

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

    def is_agree(self) -> bool:
        """Функция состояния.

        Проверяет, ответил ли пользователем согласием.

        Returns:
          True, если пользователь согласился.
        """
        return self.command == ServiceCommands.AGREE

    def is_disagree(self):
        """Функция состояния.

        Проверяет, ответил ли пользователем отказом.

        Returns:
          True, если пользователь отказался.
        """
        return self.command == ServiceCommands.DISAGREE
