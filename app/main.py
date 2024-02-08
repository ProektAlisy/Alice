"""
Точка входа в приложение.
"""
from typing import Optional

from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel

from app.command_classes import Action, skill
from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
    ORDERED_TRIGGERS,
)
from app.constants.commands import ServiceCommands
from app.constants.quiz.intents import Intents
from app.utils import (
    get_all_commands,
    get_last_in_history,
    get_trigger_by_command,
    is_alice_commands,
    last_trigger,
    next_trigger,
)


class RequestData(BaseModel):
    session: dict
    request: dict
    state: Optional[dict]


application = FastAPI()


@application.post(
    "/",
    tags=["Alice project"],
    summary="Диалог с Алисой.",
)
async def root(data: RequestData):
    command = data.request.get("command")
    nlu = data.request.get("nlu")
    intents = []
    if nlu:
        intents = nlu.get("intents", [])
    is_new = data.session.get("new")

    try:
        session_state = data.state.get("session")
    except AttributeError:
        session_state = {}

    skill.load_session_state(session_state)
    all_commands = get_all_commands(COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)
    skill.command = command

    if is_new or command in all_commands or is_alice_commands(command):
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
    command_instance = Action()
    if skill.state == "take_quiz":
        result, answer = skill.quiz_skill.execute_command(command, intents)
        if result:
            return {
                "response": {
                    "text": answer,
                    "end_session": False,
                },
                "session_state": skill.dump_session_state(),
                "version": "1.0",
            }
    if Intents.TAKE_QUIZ in intents:
        skill.machine.set_state("take_quiz")
        result, answer = skill.quiz_skill.execute_command(command, intents)
    elif not command and is_new:
        answer = Answers.FULL_GREETINGS
    elif command.lower() == ServiceCommands.REPEAT:
        answer = command_instance.execute(skill, last_trigger(skill.history))
    elif is_alice_commands(command):
        answer = Answers.STANDARD_ALICE_COMMAND
    elif command.lower() in all_commands:
        skill.is_to_progress = True
        greetings = Answers.SMALL_GREETINGS if is_new else ""
        answer = greetings + command_instance.execute(
            skill,
            get_trigger_by_command(
                command,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            ),
        )
    elif command == ServiceCommands.AGREE:
        skill.is_to_progress = True
        answer = command_instance.execute(
            skill,
            skill.next_trigger_by_progress(
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            ),
        )
    elif command == ServiceCommands.DISAGREE:
        skill.is_to_progress = False
        answer = command_instance.execute(
            skill,
            next_trigger(get_last_in_history(skill.history), ORDERED_TRIGGERS),
        )
    else:
        answer = skill.dont_understand()
    if skill.is_completed():
        answer = Answers.ALL_COMPLETED
        skill.progress = []
    ic(command, skill.state, skill.progress, skill.history, skill.max_progress)

    return {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "session_state": skill.dump_session_state(),
        "version": "1.0",
    }
