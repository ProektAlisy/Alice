import logging

from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel
from transitions import MachineError

from app.constants.answers import Answers
from app.machine import FiniteStateMachine

from app.utils import get_first_elements, get_trigger_by_command
from app.constants.user_commands import Commands, Triggers
from command_classes import commands, NextCommand, skill


#
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s, %(levelname)s, %(message)s",
# )
# logger = logging.getLogger(__name__)


class RequestData(BaseModel):
    session: dict
    request: dict


application = FastAPI()


@application.post(
    "/",
    tags=["Alice project"],
    summary="Диалог с Алисой.",
)
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
    ic(command, skill.state)
    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
