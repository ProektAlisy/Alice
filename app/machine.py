import logging

from icecream import ic
from transitions import Machine

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
)
from app.constants.skill_transitions import TRANSITIONS
from app.constants.states import STATES, DISAGREE_STATES
from app.utils import (
    get_func_answers_command,
    get_trigger_by_command,
)

logging.basicConfig(level=logging.INFO)


class FiniteStateMachine(object):
    states = STATES + DISAGREE_STATES

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
        self.max_progress = len(self.states)
        self.create_agree_functions()
        self.create_disagree_functions()

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

    def get_exit(self):
        self.message = Answers.EXIT_FROM_SKILL

    def generate_function(self, name, message, command):
        def func():
            self.message = message
            # if name in GetFunc.NOT_CORE_COMMANDS:
            #     self._save_state()
            self._save_progress(
                get_trigger_by_command(
                    command,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                ),
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

    def create_disagree_functions(self):
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

    def is_agree(self):
        ic("is_agree")
        ic(self.command == "да")
        return self.command == "да"

    def is_disagree(self):
        ic(self.command == "нет")
        return self.command == "нет"
