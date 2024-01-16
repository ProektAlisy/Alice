import logging

from fastapi import FastAPI
from pydantic import BaseModel
from transitions import MachineError

from answers import Answers
from machine import FiniteStateMachine
from icecream import ic

from user_commands import Commands


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)


class RequestData(BaseModel):
    session: dict
    request: dict


app = FastAPI()

skill = FiniteStateMachine("Собака-поводырь")


class Command:
    def execute(self, skill: FiniteStateMachine) -> str:
        raise NotImplementedError


class InfoCenterCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        try:
            skill.trigger_info_about_center()
            skill.save_progress("info_center")
        except MachineError:
            logger.debug(
                f"Команда вызвана из состояния {skill.state}, "
                f"а не из start"
            )
            skill.data["message"] = "Отсюда нельзя вызвать эту команду"
        return skill.data["message"]


class InfoPersonalCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        try:
            skill.trigger_info_about_center_personal()
            skill.save_progress("info_center_personal")
        except MachineError:
            logger.debug(
                f"Команда вызвана из состояния {skill.state}, "
                f"а не из start"
            )
            skill.data["message"] = "Отсюда нельзя вызвать эту команду"
        return skill.data["message"]


class ServicesForBlindCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        try:
            skill.trigger_services_for_blind()
            skill.save_progress("services_for_blind")
        except MachineError:
            logger.debug(
                f"Команда вызвана из состояния {skill.state}, "
                f"а не из start"
            )
            skill.data["message"] = "Отсюда нельзя вызвать эту команду"
        return skill.data["message"]


class HelpCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        skill.trigger_help()
        return skill.data["message"]


class HelpPhraseCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        skill.trigger_help_phrase()
        return skill.data["message"]


class HelpNavigationCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        skill.trigger_help_navigation()
        return skill.data["message"]


class HelpExitCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        skill.from_help()
        return skill.data["message"]


class ExitCommand(Command):
    def execute(self, skill: FiniteStateMachine) -> str:
        return skill.data["message"]


command_mapping = {
    Commands.INFO_ABOUT_CENTER: InfoCenterCommand,
    Commands.INFO_ABOUT_CENTER_PERSONAL: InfoPersonalCommand,
    Commands.HELP: HelpCommand,
    Commands.HELP_PHRASE: HelpPhraseCommand,
    Commands.HELP_NAVIGATION: HelpNavigationCommand,
    Commands.HELP_EXIT: HelpExitCommand,
    Commands.EXIT: ExitCommand,
    Commands.SERVICES_FOR_BLIND: ServicesForBlindCommand,
}


@app.post("/")
async def root(data: RequestData):
    command = data.request.get("command")
    is_new = data.session.get("new")
    ic(data.session, data.request)

    if command.lower() == "выход":
        answer = "До новых встреч!"
        return {
            "response": {
                "text": answer,
                "end_session": True,
            },
            "version": "1.0",
        }

    command_class = command_mapping.get(command.lower(), None)
    ic(command, command_class)

    if not command.lower() and is_new:
        answer = Answers.FULL_GREETINGS
    elif command_class:
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        command_instance = command_class()
        answer = greetings + command_instance.execute(skill)
    else:
        answer = Answers.DONT_UNDERSTAND

    ic(command, skill.state, skill.saved_state)
    ic(skill.progress)
    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
