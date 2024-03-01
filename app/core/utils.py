from pydantic import BaseModel
from pymongo.collection import Collection

from app.constants.states import POSSIBILITIES_STATE
from app.core.exceptions import APIError


def next_state(state: str, states: list) -> str | None:
    """Находим следующее состояние в списке состояний после заданного.

    Args:
        state: Текущее состояние.
        states: Список всех состояний.

    Returns:
        Следующее состояние или None.
    """
    try:
        index = states.index(state)
    except ValueError:
        return POSSIBILITIES_STATE
    if index < len(states) - 1:
        return states[index + 1]
    if index == len(states) - 1:
        return states[0]
    return None


def find_previous_state(
    state: str,
    ordered_states: list[str],
) -> str | None:
    """Возвращает предыдущее состояние.

    Args:
        state: Текущее состояние.
        ordered_states: Список всех состояний по порядку.

    Returns:
        Предыдущее состояние или None.
    """
    index = ordered_states.index(state)
    if index > 0:
        return ordered_states[index - 1]
    return None  # Если элемент является первым в списке


def get_states_by_command(
    command: str,
    intents: dict[str],
    structure: tuple,
) -> str | None:
    """Возвращает состояние, соответствующее заданной команде.

    Args:
        command: Команда.
        intents: Список распознанных интентов команды.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Состояние, соответствующее команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_commands in structure:
        if (
            state_commands[0].lower() == command
            or state_commands[5] in intents
        ):
            return state_commands[1]
    return None


def get_disagree_answer_by_state(state: str, structure: tuple):
    """Возвращает соответствующий отрицательный ответ.

    Args:
        state: состояние в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Триггер, соответствующий команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_commands in structure:
        if state_commands[1] == state:
            return state_commands[4]
    return None


def get_states_by_order(
    states_com_ans: list[tuple[str, str, str, str, str, str]],
) -> list[str]:
    """Возвращает список состояний.

    Порядок определяется по соответствию состоянию команде из списка
    STATES.

    Returns:
        Список состояний.
    """
    states = []
    for state_commands in states_com_ans:
        states.append(state_commands[1])
    return states


def get_all_commands(structure: tuple) -> list[str]:
    """Возвращает список команд.

    Returns:
        Список команд.
    """
    commands = []
    for state_commands in structure:
        commands.append(state_commands[0].lower())
    return commands


def is_alice_commands(command: str) -> bool:
    """Проверяет, является ли команда командами Алисы.

    Args:
        command: Команда пользователя.

    Returns:
        True, если команда является командой Алисы, иначе False.
    """
    with open(
        "app/constants/alice_commands.txt",
        "r",
        encoding="utf-8",
    ) as file:
        commands = [line.strip() for line in file]
    return command in commands


def last_states(states: list) -> str:
    """Возвращает последнее состояние.

    Args:
        states: список состояний.

    Returns:
        Последнее состояние.
    """
    try:
        result = states[-1]
    except (IndexError, TypeError):
        result = None
    return result


def read_from_db(collection: Collection):
    """Считываем из БД.

    Считываем ключи(название возможности) и ответы, которые преобразует в
    словарь.

    Args:
        collection: Коллекция в БД.

    Returns:
        Словарь вида {key: answer}
    """
    documents = collection.find({}, projection={"_id": False})
    return {doc["key"]: doc["answer"] for doc in documents}


def get_after_answer_by_state(
    state: str,
    structure: list[tuple[str]],
) -> str:
    """Возвращает соответствующий направляющий вопрос.

    Args:
        state: Состояние, в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Состояние, соответствующее команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_com_ans in structure:
        if state_com_ans[1] == state:
            return state_com_ans[3]
    return ""


def get_answer_by_state(
    state: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующий ответ.

    Args:
        state: Состояние, в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Состояние, соответствующее команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_com_ans in structure:
        if state_com_ans[1] == state:
            return state_com_ans[2]
    return ""


def get_states_group_by_state(
    state: str,
    structure: list[tuple[str]],
) -> tuple[str] | None:
    """Получаем группу состояний.

    Необходимо для пропуска сразу целого раздела, в случае отказа пользователя.

    Args:
        state: Состояние, в которое переходим.
        structure: Структура.

    Returns:
        Группа состояний.
    """
    for group_states in structure:
        if state in group_states:
            return group_states
    return None


def get_last_in_history(history: list[str]) -> str:
    """Получить последнее действие из истории.

    Args:
        history: Список действий (переходов) пользователя в навыке.

    Returns:
        Последнее действие из истории.
    """
    try:
        result = history[-1]
    except (IndexError, TypeError):
        result = None
    return result


def disagree_answer_by_state(
    state: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующий ответ.

    Args:
        state: Состояние, в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Триггер, соответствующий команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_com_ans in structure:
        if state_com_ans[1] == state:
            return state_com_ans[4]
    return ""


def check_api(data: BaseModel) -> None:
    try:
        _ = data.request["command"]
        _ = data.request["nlu"]
        _ = data.session["new"]
        _ = data.state["session"]
    except KeyError:
        raise APIError


def get_api_data(data: BaseModel) -> tuple[str, dict[str], bool, dict[str]]:
    command = data.request.get("command")
    nlu = data.request.get("nlu")
    is_new = data.session.get("new")
    session_state = data.state.get("session")
    if nlu:
        intents = nlu.get("intents", {})
    else:
        intents = {}
    return command, intents, is_new, session_state


def compose_message(answer: str, after_answer: str) -> str:
    """Составляем сообщение пользователю.

    Args:
        answer: Основная часть ответа.
        after_answer: Часть ответа с подсказкой о продолжении.

    Returns:
        Полный ответ.
    """
    return f"{answer} sil <[400]> {after_answer}"


def get_state_by_answer(
    answer: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующее состояние.

    Args:
        answer: Состояние, в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Состояние, соответствующее команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_com_ans in structure:
        if state_com_ans[2] == answer:
            return state_com_ans[1]
    return ""


def get_state_by_after_answer(
    after_answer: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующее состояние.

    Args:
        after_answer: Состояние, в которое переходим.
        structure: Структура, содержащая соответствующие команды и состояния.

    Returns:
        Состояние, соответствующее команде. Если соответствующее состояние
        не найдено, возвращает None.
    """
    for state_com_ans in structure:
        if state_com_ans[3] == after_answer:
            return state_com_ans[1]
    return ""
