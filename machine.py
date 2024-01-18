from transitions import Machine
import logging

from answers import Answers
from states import TRANSITIONS
from utils import get_func_answers_command, get_trigger_by_command


logging.basicConfig(level=logging.DEBUG)


class FiniteStateMachine(object):
    states = [
        "start",
        "help",
        "services_for_blind",
    ]

    def __init__(self):
        self.message = ""
        self.saved_state = None
        self.progress = None
        self.machine = Machine(
            model=self,
            states=FiniteStateMachine.states,
            transitions=TRANSITIONS,
            initial="start",
        )
        self.create_functions()

    def _save_state(self):
        self.saved_state = self.state

    def _save_progress(self, step: str) -> None:
        if self.progress is None:
            self.progress = []
        if step not in self.progress:
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
            self._save_progress(get_trigger_by_command(command))
        setattr(self, name, func)

    def create_functions(self):
        [
            self.generate_function(func_name, answer, command)
            for func_name, answer, command in get_func_answers_command()
        ]
