from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel

from app.command_classes import NextCommand, skill
from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
)
from app.constants.commands import ServiceCommands
from app.utils import (
    get_all_commands,
    get_next_trigger,
    get_trigger_by_command,
    is_alice_commands,
    is_completed,
    last_trigger,
)


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
    all_commands = get_all_commands(COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)
    skill.command = command

    if is_new or command in all_commands:
        skill.incorrect_answers = 0

    if command.lower() == ServiceCommands.EXIT:
        answer = Answers.EXIT_FROM_SKILL
        return {
            "response": {
                "text": answer,
                "end_session": True,
            },
            "version": "1.0",
        }
    command_instance = NextCommand()
    if not command and is_new:
        answer = Answers.FULL_GREETINGS
    elif is_completed(skill):
        answer = Answers.ALL_COMPLETED
    elif command.lower() == ServiceCommands.REPEAT:
        command_instance = NextCommand()
        answer = command_instance.execute(skill, last_trigger(skill))
    elif is_alice_commands(command):
        answer = Answers.STANDARD_ALICE_COMMAND
    elif command.lower() in all_commands:
        skill.flag = True
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        answer = greetings + command_instance.execute(
            skill,
            get_trigger_by_command(
                command,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            ),
        )
    elif command in (ServiceCommands.AGREE, ServiceCommands.DISAGREE):
        skill.flag = True if command == ServiceCommands.AGREE else False
        answer = command_instance.execute(
            skill,
            get_next_trigger(skill, COMMANDS_TRIGGERS_GET_FUNC_ANSWERS),
        )
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
