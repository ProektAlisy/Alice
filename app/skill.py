from app.constants.comands_states_answers import ERROR_MESSAGE
from app.core.action_classes import Action
from app.core.command_classes import (
    AgreeCommand,
    AliceCommandsCommand,
    AllCommandsCommand,
    Command,
    DisagreeCommand,
    DontUnderstandCommand,
    ExitCommand,
    GreetingsCommand,
    HelpCommandsCommand,
    ManualTrainingCommand,
    ManualTrainingSetState,
    QuizCommand,
    QuizSetState,
    RepeatCommand,
)
from app.core.utils import (
    get_api_data,
    get_error_response,
    limit_response_text_length,
)
from app.machine import FiniteStateMachine
from app.schemas import RequestData, ResponseData

skill = FiniteStateMachine()
command_instance = Action()

commands = [
    QuizSetState(skill, command_instance),
    QuizCommand(skill, command_instance),
    ManualTrainingSetState(skill, command_instance),
    ManualTrainingCommand(skill, command_instance),
    GreetingsCommand(skill, False),
    RepeatCommand(skill, command_instance),
    AliceCommandsCommand(skill, command_instance),
    AllCommandsCommand(skill, command_instance),
    AgreeCommand(skill, command_instance),
    DisagreeCommand(skill, command_instance),
    HelpCommandsCommand(skill, command_instance),
    ExitCommand(skill, command_instance),
    DontUnderstandCommand(skill, command_instance),
]


def update_greetings_command(commands: list[Command], is_new: bool) -> None:
    """Обновляет обработчик команды GreetingsCommand согласно значению is_new.

    Args:
        commands: Список всех обработчиков команд навыка.
        is_new: Признак начального запуска навыка из параметров запроса.
    """
    for i, command in enumerate(commands):
        if isinstance(command, GreetingsCommand):
            commands[i] = GreetingsCommand(skill, is_new)
            break


def get_skill_response(data: RequestData) -> ResponseData:
    """Анализирует запрос от диалогов и формирует ответ навыка.

    Args:
        data: Объект запроса от Яндекс.Диалогов.

    Returns:
        Сформированный объект ответа в Яндекс.Диалоги.
    """
    command, intents, is_new, session_state = get_api_data(data)
    skill.load_session_state(session_state)
    skill.command = command
    skill.intents = intents
    # update GreetingsCommand state according current is_new
    update_greetings_command(commands, is_new)

    result = None
    for command_obj in commands:
        if command_obj.condition(intents, command, is_new):
            result = command_obj.execute(intents, command, is_new)
            # повторно выполнить dump_session_state (поменялся progress)
            result.session_state = skill.dump_session_state()
            limit_response_text_length(result.response)
            break
    # ic(command, skill.progress, skill.history)
    skill.previous_command = command
    if result is None:
        # команда не была никем обработана и нет ответа
        result = get_error_response(
            answer_text=ERROR_MESSAGE, session_state=skill.dump_session_state()
        )
    return result
