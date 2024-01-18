from icecream import ic
from transitions import Machine
import logging

from answers import Answers
from states import TRANSITIONS
from user_commands import Commands, Default


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

    # def get_training_center(self):
    #     self.message = Answers.INFO_ABOUT_CENTER
    #     self._save_progress(
    #         Default.TRIGGERS_COMMANDS.get(Commands.ABOUT_TRAINING_CENTER)
    #     )

    # def get_staff(self):
    #     self.message = Answers.INFO_ABOUT_STAFF
    #     self._save_progress(
    #         Default.TRIGGERS_COMMANDS.get(Commands.ABOUT_STAFF)
    #     )
    #
    # def get_services_for_blind(self):
    #     self.message = Answers.SERVICES_FOR_BLIND
    #     self._save_progress(
    #         Default.TRIGGERS_COMMANDS.get(
    #             Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE
    #         )
    #     )

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

    def get_service_for_blind(self):
        self.message = Answers.SERVICES_FOR_BLIND

    def generate_function(self, name, message, command):
        def func():
            self.message = message
            self._save_progress(Default.TRIGGERS_COMMANDS.get(command))

        setattr(self, name, func)

    def create_functions(self):
        self.generate_function(
            "get_training_center",
            Answers.INFO_ABOUT_CENTER,
            Commands.ABOUT_TRAINING_CENTER,
        )
        self.generate_function(
            "get_staff", Answers.INFO_ABOUT_STAFF, Commands.ABOUT_STAFF
        )
        self.generate_function(
            "get_services_for_blind",
            Answers.SERVICES_FOR_BLIND,
            Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
        )
