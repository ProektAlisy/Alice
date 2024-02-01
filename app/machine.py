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
        else:
            self.message = Answers.DONT_UNDERSTAND_MORE_THAN_ONCE
        return self.message

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
