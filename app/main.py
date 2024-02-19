"""
Точка входа в приложение.
"""

from typing import Optional

from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel

from app.constants.comands_triggers_answers import another_answers_documents
from app.core.action_classes import Action
from app.core.command_classes import (
    AgreeCommand,
    AliceCommandsCommand,
    AllCommandsCommand,
    DisagreeCommand,
    ExitCommand,
    GreetingsCommand,
    ManualTrainingCommand,
    ManualTrainingSetState,
    QuizCommand,
    QuizSetState,
    RepeatCommand,
    skill,
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

    skill.command = command
    command_instance = Action()

    commands = [
        QuizSetState(skill, command_instance),
        QuizCommand(skill, command_instance),
        ManualTrainingSetState(skill, command_instance),
        ManualTrainingCommand(skill, command_instance),
        GreetingsCommand(skill, is_new),
        RepeatCommand(skill, command_instance),
        AliceCommandsCommand(skill, command_instance),
        AllCommandsCommand(skill, command_instance),
        AgreeCommand(skill, command_instance),
        DisagreeCommand(skill, command_instance),
        ExitCommand(skill, command_instance),
    ]
    answer = skill.dont_understand()
    directives = {}
    for command_obj in commands:
        if command_obj.condition(intents, command, is_new):
            # спец-обработчик для аудио обучения по методичке, т.к. еще возвращает directives
            if type(command_obj) in [
                ManualTrainingSetState,
                ManualTrainingCommand,
            ]:
                answer, directives = command_obj.execute(
                    intents,
                    command,
                    is_new,
                )
            else:
                ic(command_obj)
                answer = command_obj.execute(intents, command, is_new)
            break
    if skill.is_completed():
        answer = another_answers_documents.get("all_completed", "")
        skill.progress = []

    end_session = (
        True
        if answer == another_answers_documents.get("exit_from_skill", "")
        else False
    )
    ic(command, skill.progress, skill.history)
    skill.previous_command = command
    return {
        "response": {
            "text": answer,
            "end_session": end_session,
            "directives": directives,
        },
        "session_state": skill.dump_session_state(),
        "version": "1.0",
    }
