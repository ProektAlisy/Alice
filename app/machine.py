from icecream import ic
from transitions import Machine
import logging

from app.constants.answers import Answers
from app.constants.states import TRANSITIONS
from app.constants.user_commands import Commands, Default


logging.basicConfig(level=logging.DEBUG)


class FiniteStateMachine(object):
    states = [
        "start",
        "help",
        "services_for_blind",
    ]

    def __init__(self, name):
        self.name = name
        self.message = ""
        self.saved_state = None
        self.progress = None
        self.machine = Machine(
            model=self,
            states=FiniteStateMachine.states,
            transitions=TRANSITIONS,
            initial="start",
        )

    def _save_state(self):
        self.saved_state = self.state

    def save_progress(self, step: str) -> None:
        if self.progress is None:
            self.progress = []
        if step not in self.progress:
            self.progress.append(step)

    def _return_to_original_state(self):
        self.machine.set_state(self.saved_state)

    def get_training_center(self):
        self.message = Answers.INFO_ABOUT_CENTER
        self.save_progress(
            Default.TRIGGERS_COMMANDS.get(Commands.ABOUT_TRAINING_CENTER)
        )

    def get_staff(self):
        self.message = Answers.INFO_ABOUT_STAFF
        self.save_progress(Default.TRIGGERS_COMMANDS.get(Commands.ABOUT_STAFF))

    def get_services_for_blind(self):
        self.message = Answers.SERVICES_FOR_BLIND
        self.save_progress(
            Default.TRIGGERS_COMMANDS.get(
                Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE
            )
        )

    def get_help(self):
        self.saved_state = self.state
        self.message = (
            "Здесь вы можете узнать фразы взаимодействия или "
            "получить помощь с навигацией по навыку!"
        )

    def get_help_phrase(self):
        self.message = "Вот это фразы взаимодействия с навыком"

    def get_help_navigation(self):
        self.message = "Вот помощь по навигации по навыку"

    def get_help_exit(self):
        self.message = "Вы вышли из помощи!"

    def get_exit(self):
        self.message = Answers.EXIT_FROM_SKILL

    def get_service_for_blind(self):
        self.message = Answers.SERVICES_FOR_BLIND
