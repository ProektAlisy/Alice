import logging

from transitions import MachineError

from app.constants.answers import Answers
from app.constants.commands_triggers_functions import (
    Commands,
    TrigComAns,
    Triggers,
)
from app.machine import FiniteStateMachine
from app.utils import transform_string

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


list_of_commands = TrigComAns.COMMAND_NAMES
list_of_commands.extend(
    [
        "HELP",
        "HELP_PHRASE",
        "HELP_NAVIGATION",
        "NEXT",
    ],
)

commands = {}
for constant in list_of_commands:
    commands.update(
        {
            getattr(Commands, constant): create_command_class(
                transform_string(constant),
                getattr(Triggers, constant),
                getattr(Answers, constant),
            ),
        },
    )
