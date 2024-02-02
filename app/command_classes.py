import logging

from transitions import MachineError

from app.constants.answers import Answers
from app.logger_initialize import logger
from app.machine import FiniteStateMachine

skill = FiniteStateMachine()


class Command:
    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> str:
        raise NotImplementedError


class Action(Command):
    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> str:
        if trigger_name is None:
            return Answers.HELP_MAIN
        try:
            skill_obj.trigger(trigger_name)
        except MachineError:
            logger.debug(f"Команда вызвана из состояния {skill_obj.state}")
            skill_obj.message = "Отсюда нельзя вызвать эту команду"
        return skill_obj.message
