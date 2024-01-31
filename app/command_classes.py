import logging

from transitions import MachineError

from app.constants.answers import Answers
from app.machine import FiniteStateMachine

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
