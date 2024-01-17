import logging

from constants import TRANSITIONS
from transitions import Machine

logging.basicConfig(level=logging.DEBUG)


class Skills(object):
    states = [
        "start",
        "info_center",
        "info_personal",
        "help",
    ]

    transitions = TRANSITIONS

    def __init__(self, name):
        self.name = name
        self.data = {}
        self.saved_state = None
        self.machine = Machine(
            model=self,
            states=Skills.states,
            transitions=Skills.transitions,
            initial="start",
        )

    def _save_state(self):
        self.saved_state = self.state

    def _return_to_original_state(self):
        self.machine.set_state(self.saved_state)

    def get_info_about_center(self):
        self.data = {"message": "Наш центр самый самый и все такое"}

    def get_info_about_center_personal(self):
        self.data = {"message": "Вот наш персонал: Маша, Витя и Леонид"}

    def get_info(self):
        self.data = {"message": "Дополнительная информация"}

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
        self.data = {"message": "Вы вышли из помощи"}
