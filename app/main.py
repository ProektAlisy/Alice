"""
Точка входа в приложение.
"""

from typing import Optional

from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel

from app.core.action_classes import Action
from app.core.command_classes import (
    AgreeCommand,
    AliceCommandsCommand,
    AllCommandsCommand,
    DisagreeCommand,
    ExitCommand,
    GreetingsCommand,
    QuizCommand,
    QuizSetState,
    RepeatCommand,
    skill,
)
from app.constants.answers import Answers


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
    skill.command = command
    command_instance = Action()

    commands = [
        QuizSetState(skill, command_instance),
        QuizCommand(skill, command_instance),
        GreetingsCommand(skill, is_new),
        RepeatCommand(skill, command_instance),
        AliceCommandsCommand(skill, command_instance),
        AllCommandsCommand(skill, command_instance),
        AgreeCommand(skill, command_instance),
        DisagreeCommand(skill, command_instance),
        ExitCommand(skill, command_instance),
    ]
    answer = skill.dont_understand()

    for command_obj in commands:
        if command_obj.condition(intents, command, is_new):
            answer = command_obj.execute(intents, command, is_new)
            break

    if skill.is_completed():
        answer = Answers.ALL_COMPLETED
        skill.progress = []

    end_session = True if answer == Answers.EXIT_FROM_SKILL else False
    ic(command, skill.state, skill.progress, skill.history)
    skill.previous_command = command
    return {
        "response": {
            "text": answer,
            "end_session": end_session,
        },
        "session_state": skill.dump_session_state(),
        "version": "1.0",
    }
