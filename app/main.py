from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel

from app.command_classes import NextCommand, commands, skill
from app.constants.answers import Answers
from app.constants.commands_triggers_functions import Commands
from app.utils import (get_all_commands, get_next_trigger, is_alice_commands,
                       is_completed)


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

    all_commands = get_all_commands()
    if is_new or command in all_commands:
        skill.incorrect_answers = 0

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
    if not command and is_new:
        answer = Answers.FULL_GREETINGS
    elif command_class and command_class.__name__ == "NextCommand":
        command_instance = NextCommand()
        if is_completed(skill):
            answer = Answers.ALL_COMPLETED
        else:
            answer = command_instance.execute(
                skill,
                get_next_trigger(skill.progress),
            )
    elif command == Commands.REPEAT:
        command_instance = NextCommand()
        answer = command_instance.execute(skill, skill.progress[-1])
    elif command_class:
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        command_instance = command_class()
        answer = greetings + command_instance.execute(skill)
    elif is_alice_commands(command):
        answer = Answers.STANDART_ALICE_COMMAND
    else:
        answer = skill.dont_understand()
    ic(command, skill.state, skill.progress)
    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
