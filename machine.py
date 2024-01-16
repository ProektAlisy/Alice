from icecream import ic
from transitions import Machine
import logging

from answers import Answers
from states import TRANSITIONS


logging.basicConfig(level=logging.DEBUG)


class FiniteStateMachine(object):
    states = [
        "start",
        "info_center",
        "info_personal",
        "help",
        "services_for_blind",
    ]

    def __init__(self, name):
        self.name = name
        self.data = {}
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
        ic(self.saved_state)

    def save_progress(self, step: str) -> None:
        if self.progress is None:
            self.progress = set()
        self.progress.add(step)

    def _return_to_original_state(self):
        self.machine.set_state(self.saved_state)

    def get_info_about_center(self):
        self.data = {"message": "Наш центр самый самый и все такое"}

    def get_info_about_center_personal(self):
        self.data = {"message": "Вот наш персонал: Маша, Витя и Леонид"}
    #
    # def get_info(self):
    #     self.data = {"message": "Дополнительная информация"}

    def get_help(self):
        self.saved_state = self.state
        self.data = {
            "message": "Здесь вы можете узнать фразы взаимодействия или "
            "получить помощь с навигацией по навыку!"
        }

    def get_help_phrase(self):
        self.data = {"message": "Вот это фразы взаимодействия с навыком"}

    def get_help_navigation(self):
        self.data = {"message": "Вот помощь по навигации по навыку"}

    def get_help_exit(self):
        self.data = {"message": "Вы вышли из помощи!"}

    def get_services_for_blind(self):
        self.data = {"message": Answers.SERVICES_FOR_BLIND}

    def get_exit(self):
        self.data = {"message": "Вы вышли из навыка!"}

    def get_service_for_blind(self):
        self.data = {
            "message": Answers.SERVICES_FOR_BLIND
        }
