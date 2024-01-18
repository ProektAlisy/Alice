import logging

from fastapi import FastAPI
from pydantic import BaseModel
from transitions import MachineError

from answers import Answers
from machine import FiniteStateMachine
from icecream import ic

from user_commands import Commands, Default


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)


class RequestData(BaseModel):
    session: dict
    request: dict


app = FastAPI()

skill = FiniteStateMachine()

#
# class Command:
#     @staticmethod
#     def execute(
#         skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         raise NotImplementedError
#
#
# class NextCommand(Command):
#     @staticmethod
#     def execute(
#         skill: FiniteStateMachine, trigger: str | None = None
#     ) -> str:
#         try:
#             skill.trigger(trigger)
#         except MachineError:
#             logger.debug(
#                 f"Команда вызвана из состояния {skill.state}, "
#                 f"а не из start"
#             )
#             skill.message = "Отсюда нельзя вызвать эту команду"
#         return skill.message
#
#
# class TrainingCenter(Command):
#     @staticmethod
#     def execute(
#         skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         try:
#             skill.trigger_training_center()
#         except MachineError:
#             logger.debug(
#                 f"Команда вызвана из состояния {skill.state}, "
#                 f"а не из start"
#             )
#             skill.message = "Отсюда нельзя вызвать эту команду"
#         return skill.message
#
#
# class Staff(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         try:
#             skill.trigger_staff()
#         except MachineError:
#             logger.debug(
#                 f"Команда вызвана из состояния {skill.state}, "
#                 f"а не из start"
#             )
#             skill.message = "Отсюда нельзя вызвать эту команду"
#         return skill.message
#
#
# class ServicesForBlindCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         try:
#             skill.trigger_services_for_blind()
#         except MachineError:
#             logger.debug(
#                 f"Команда вызвана из состояния {skill.state}, "
#                 f"а не из start"
#             )
#             skill.message = "Отсюда нельзя вызвать эту команду"
#         return skill.message
#
#
# class HelpCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         skill.trigger_help()
#         return skill.message
#
#
# class HelpPhraseCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         skill.trigger_help_phrase()
#         return skill.message
#
#
# class HelpNavigationCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         skill.trigger_help_navigation()
#         return skill.message
#
#
# class HelpExitCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         skill.from_help()
#         return skill.message
#
#
# class ExitCommand(Command):
#     def execute(
#         self, skill: FiniteStateMachine, target_state: str | None = None
#     ) -> str:
#         return skill.message


# command_mapping = {
#     Commands.ABOUT_TRAINING_CENTER: TrainingCenter,
#     Commands.ABOUT_STAFF: Staff,
#     Commands.HELP: HelpCommand,
#     Commands.HELP_PHRASE: HelpPhraseCommand,
#     Commands.HELP_NAVIGATION: HelpNavigationCommand,
#     Commands.HELP_EXIT: HelpExitCommand,
#     Commands.EXIT: ExitCommand,
#     Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE: ServicesForBlindCommand,
#     Commands.NEXT: NextCommand,
# }


class Command:
    @staticmethod
    def execute(
        skill: FiniteStateMachine, target_state: str | None = None
    ) -> str:
        raise NotImplementedError


class NextCommand(Command):
    @staticmethod
    def execute(
        skill: FiniteStateMachine, trigger: str | None = None
    ) -> str:
        try:
            skill.trigger(trigger)
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
                    f"Команда вызвана из состояния {skill.state}, а не из start"
                )
                skill.message = "Отсюда нельзя вызвать эту команду"
            return skill.message

    CustomCommand.__name__ = name
    return CustomCommand


# Создаем классы команд динамически
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
        "Помощь по навыку",
    ),
    Commands.HELP_PHRASE: create_command_class(
        "HelpPhraseCommand",
        "trigger_help_phrase",
        "Фразы взаимодействия с навыком",
    ),
    Commands.HELP_NAVIGATION: create_command_class(
        "HelpNavigationCommand",
        "trigger_help_navigation",
        "Помощь по навигации по навыку",
    ),
}


command_mapping = commands


@app.post("/")
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

    command_class = command_mapping.get(command.lower(), None)
    ic(command_class.__name__)
    if not command.lower() and is_new:
        answer = Answers.FULL_GREETINGS
    elif command_class.__name__ == "NextCommand":
        command_instance = NextCommand()
        if len(skill.progress) < len(Default.ORDER):
            next_state = Default.ORDER[len(skill.progress)]
            ic(next_state)
            answer = command_instance.execute(
                skill, Default.TRIGGERS_COMMANDS[next_state]
            )
        else:
            answer = Answers.ALL_COMPLETED
    elif command_class:
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        command_instance = command_class()
        answer = greetings + command_instance.execute(skill)
    else:
        answer = Answers.DONT_UNDERSTAND
    ic(answer, skill.state, skill.progress)
    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
