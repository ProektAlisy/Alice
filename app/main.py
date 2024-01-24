import logging

from fastapi import FastAPI
from pydantic import BaseModel
from transitions import MachineError

from app.constants.answers import Answers
from app.constants.user_commands import Commands
from app.machine import FiniteStateMachine
from app.utils import get_first_elements, get_trigger_by_command

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)


class RequestData(BaseModel):
    session: dict
    request: dict


application = FastAPI()

skill = FiniteStateMachine()


class Command:
    @staticmethod
    def execute(
        skill: FiniteStateMachine, target_state: str | None = None
    ) -> str:
        raise NotImplementedError


class NextCommand(Command):
    @staticmethod
    def execute(
        skill: FiniteStateMachine, trigger_name: str | None = None
    ) -> str:
        try:
            skill.trigger(trigger_name)
        except MachineError:
            logger.debug(
                f"Команда вызвана из состояния {skill.state}, "
                f"а не из start"
            )
            skill.message = "Отсюда нельзя вызвать эту команду"
        return skill.message


def create_command_class(name: str, trigger_name: str, message: str):
    class CustomCommand(Command):
        def execute(
            self, skill: FiniteStateMachine, target_state: str | None = None
        ) -> str:
            try:
                skill.trigger(trigger_name)
                skill.message = message
            except MachineError:
                logger.debug(
                    f"Команда вызвана из состояния {skill.state}, "
                    f"а не из start"
                )
                skill.message = "Отсюда нельзя вызвать эту команду"
            return skill.message

    CustomCommand.__name__ = name
    return CustomCommand


commands = {
    Commands.NEXT: create_command_class(
        "NextCommand",
        "trigger",
        Answers.INFO_ABOUT_CENTER,
    ),
    Commands.ABOUT_TRAINING_CENTER: create_command_class(
        "TrainingCenterCommand",
        "trigger_training_center",
        Answers.INFO_ABOUT_CENTER,
    ),
    Commands.ABOUT_STAFF: create_command_class(
        "StaffCommand",
        "trigger_staff",
        Answers.INFO_ABOUT_STAFF,
    ),
    Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE: create_command_class(
        "ServicesForBlindCommand",
        "trigger_services_for_blind",
        Answers.SERVICES_FOR_BLIND,
    ),
    Commands.HELP: create_command_class(
        "HelpCommand",
        "trigger_help",
        Answers.HELP_MAIN,
    ),
    Commands.HELP_PHRASE: create_command_class(
        "HelpPhraseCommand",
        "trigger_help_phrase",
        Answers.HELP_PHRASE,
    ),
    Commands.HELP_NAVIGATION: create_command_class(
        "HelpNavigationCommand",
        "trigger_help_navigation",
        Answers.HELP_NAVIGATION,
    ),
}


@application.post("/", tags=['Alice project'], summary='Диалог с Алисой.')
async def root(data: RequestData):
    command = data.request.get("command")
    is_new = data.session.get("new")

    if command.lower() == Commands.EXIT:
        answer = Answers.EXIT_FROM_SKILL
        return {
            "response": {
                "text": answer,
                "end_session": True,
            },
            "version": "1.0",
        }

    command_class = commands.get(command.lower(), None)
    if not command.lower() and is_new:
        answer = Answers.FULL_GREETINGS
    elif command_class and command_class.__name__ == "NextCommand":
        command_instance = NextCommand()
        ordered_states = get_first_elements()
        if skill.progress and len(skill.progress) < len(ordered_states):
            next_command = ordered_states[len(skill.progress)]
            answer = command_instance.execute(
                skill, get_trigger_by_command(next_command)
            )
        else:
            answer = Answers.ALL_COMPLETED
    elif command_class:
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        command_instance = command_class()
        answer = greetings + command_instance.execute(skill)
    else:
        answer = Answers.DONT_UNDERSTAND
    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
