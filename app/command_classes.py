import logging

from icecream import ic
from transitions import MachineError

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import answers_documents
from app.constants.commands import (
    Commands,
)
from app.constants.states import STATES
from app.machine import FiniteStateMachine
from app.utils import transform_string, create_trigger


skill = FiniteStateMachine()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)


class Command:
    @staticmethod
    def execute(
        skill: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> str:
        raise NotImplementedError


class NextCommand(Command):
    @staticmethod
    def execute(
        skill: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> str:
        if trigger_name is None:
            return Answers.HELP_MAIN
        try:
            ic(trigger_name)
            skill.trigger(trigger_name)
        except MachineError:
            logger.debug(f"Команда вызвана из состояния {skill.state}")
            skill.message = "Отсюда нельзя вызвать эту команду"
        return skill.message


def create_command_class(name: str, trigger_name: str, message: str):
    class CustomCommand(Command):
        def execute(
            self,
            skill: FiniteStateMachine,
            target_state: str | None = None,
        ) -> str:
            try:
                skill.trigger(trigger_name)
                skill.message = message
            except MachineError:
                logger.debug(f"Команда вызвана из состояния {skill.state}")
                skill.message = "Отсюда нельзя вызвать эту команду"
            return skill.message

    CustomCommand.__name__ = name
    return CustomCommand


list_of_commands = STATES[1:]


commands = {}
for command in list_of_commands:
    commands.update(
        {
            getattr(Commands, command): create_command_class(
                transform_string(command),
                create_trigger(command),
                answers_documents.get(command),
            ),
        },
    )
commands.update(
    {
        "да": NextCommand,
    },
)
commands.update(
    {
        "нет": NextCommand,
    },
)
