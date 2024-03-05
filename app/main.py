"""
Точка входа в приложение.
"""

from fastapi import FastAPI
from icecream import ic

from app.constants.comands_states_answers import another_answers_documents
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
    HelpCommandsCommand,
)
from app.core.exceptions import APIError
from app.core.logger_initialize import logger
from app.core.utils import check_api, get_api_data, limit_response_text_length
from app.schemas import RequestData, ResponseData

application = FastAPI()


@application.post(
    "/",
    tags=["Alice project"],
    summary="Диалог с Алисой.",
)
async def root(data: RequestData) -> ResponseData:
    request_data = data.model_dump()

    try:
        check_api(data)
    except APIError:
        logger.error("Invalid request format!")
        return skill.get_output(
            "Технические проблемы на стороне Яндекса. Попробуйте позже.",
        )
    command, intents, is_new, session_state = get_api_data(data)
    skill.load_session_state(session_state)
    skill.command = command
    skill.intents = intents
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
        HelpCommandsCommand(skill, command_instance),
        ExitCommand(skill, command_instance),
    ]
    result = skill.get_output(skill.dont_understand())
    for command_obj in commands:
        if command_obj.condition(intents, command, is_new):
            result = command_obj.execute(intents, command, is_new)
            break
    if skill.is_completed():
        result = skill.get_output(
            another_answers_documents.get(
                "all_completed",
                "",
            ),
        )
        skill.progress = []
    ic(command, skill.progress, skill.history)
    skill.previous_command = command
    limit_response_text_length(result.response)
    logger.info(
        "HISTORY",
        extra={
            "request": request_data,
            "response": result,
        },
    )
    return result
