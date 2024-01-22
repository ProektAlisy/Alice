import logging

from icecream import ic
from transitions import Machine

from app.constants.answers import Answers
from app.constants.commands_triggers_functions import GetFunc
from app.constants.states import TRANSITIONS
from app.utils import get_func_answers_command, get_trigger_by_command

logging.basicConfig(level=logging.DEBUG)


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
        self.machine = Machine(
            model=self,
            states=FiniteStateMachine.states,
            transitions=TRANSITIONS,
            initial="start",
        )
        self.create_functions()

    def _save_state(self):
        """
        Save the current state to the saved_state attribute.
        """
        self.saved_state = self.state

    def _save_progress(self, step: str) -> None:
        """
        Save the progress of the step.
        """
        if self.progress is None:
            self.progress = []
        if step not in self.progress:
            self.progress.append(step)

    def _return_to_original_state(self):
        """
        Restore the object to its original state by
        setting the state to the saved state.
        """
        self.machine.set_state(self.saved_state)

    def get_help(self):
        """
        Method to retrieve help information.
        """
        self.saved_state = self.state
        self.message = Answers.HELP_MAIN

    def get_help_phrase(self):
        """
        Method to retrieve the help phrase and assign it
        to the message attribute.
        """
        self.message = Answers.HELP_PHRASE

    def get_help_navigation(self):
        """
        This function sets the 'message' attribute
        to the value of Answers.HELP_NAVIGATION.
        """
        self.message = Answers.HELP_NAVIGATION

    def get_help_exit(self):
        """
        Method to get the help exit message and assign it
        to the 'message' attribute.
        """
        self.message = Answers.EXIT_FROM_HELP

    # def get_legislation_exit(self):
    #     self.message = Answers.EXIT_FROM_LEGISLATION

    # def get_discounts_free_services_exit(self):
    #     self.message = Answers.EXIT_DISCOUNTS_AND_FREE_SERVICES

    # def get_services_for_blind_exit(self):
    #     self.message = Answers.EXIT_SERVICES_FOR_BLIND

    def get_exit(self):
        """
        Set the message attribute to indicate that
        the user is exiting from the skill.
        """
        self.message = Answers.EXIT_FROM_SKILL

    def generate_function(self, name, message, command):
        """
        Generates a function and sets it as an attribute on the instance.
        Args:
            self: The instance to set the function on.
            name: The name of the function.
            message: The message to set on the instance.
            command: The command to use for progress saving.
        """

        def func():
            self.message = message
            ic(name)
            if name in GetFunc.CORE_COMMANDS:
                print(name)
                self._save_state()
            self._save_progress(get_trigger_by_command(command))

        setattr(self, name, func)

    def create_functions(self):
        """
        Create functions using the specified parameters
        from get_func_answers_command.
        """
        [
            self.generate_function(func_name, answer, command)
            for func_name, answer, command in get_func_answers_command()
        ]
