from pydantic import BaseModel
from pymongo.collection import Collection

from app.constants.states import POSSIBILITIES_TRIGGER
from app.core.exceptions import APIError


def next_trigger(trigger: str, triggers: list) -> str | None:
    """Находим следующий триггер в списке триггеров после заданного.

    Args:
        trigger: Текущий триггер.
        triggers: Список всех триггеров.

    Returns:
        Следующий триггер или None.
    """
    try:
        index = triggers.index(trigger)
    except ValueError:
        return POSSIBILITIES_TRIGGER
    if index < len(triggers) - 1:
        return triggers[index + 1]
    if index == len(triggers) - 1:
        return triggers[0]
    return None


def find_previous_element(
    trigger: str,
    ordered_triggers: list[str],
) -> str | None:
    """Возвращает предыдущий триггер.

    Args:
        trigger: Текущий триггер.
        ordered_triggers: Список всех триггеров.

    Returns:
        Предыдущий триггер или None.
    """
    index = ordered_triggers.index(trigger)
    if index > 0:
        return ordered_triggers[index - 1]
    return None  # Если элемент является первым в списке


def get_trigger_by_command(
    command: str,
    intents: dict[str],
    structure: tuple,
) -> str | None:
    """Возвращает триггер, соответствующий заданной команде.

    Args:
        command: Команда.
        intents: Список распознанных интентов команды.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_commands in structure:
        if trig_commands[0].lower() == command or trig_commands[6] in intents:
            return trig_commands[1]
    return None


def get_disagree_answer_by_trigger(trigger: str, structure: tuple):
    """Возвращает соответствующий отрицательный ответ.

    Args:
        trigger: Триггер действия.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_commands in structure:
        if trig_commands[1] == trigger:
            return trig_commands[5]
    return None


def get_triggers_by_order(
    trig_com_ans: list[tuple[str, str, str, str, str, str, str]],
) -> list[str]:
    """Возвращает список триггеров.

    Порядок определяется по соответствию триггеру команде из списка
    TrigComAns.COMMANDS_NAMES.

    Returns:
        Список триггеров.
    """
    triggers = []
    for trig_commands in trig_com_ans:
        triggers.append(trig_commands[1])
    return triggers


def get_all_commands(structure: tuple) -> list[str]:
    """Возвращает список команд.

    Returns:
        Список команд.
    """
    commands = []
    for trig_commands in structure:
        commands.append(trig_commands[0].lower())
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


def last_trigger(triggers: list) -> str:
    """Возвращает последний триггер.

    Args:
        triggers: список триггеров.

    Returns:
        Последний триггер.
    """
    try:
        result = triggers[-1]
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


def create_func(name):
    """Создает имя функции.

    Args:
        name: Имя состояния.

    Returns:
        Имя функции
    """
    return "get_" + name


def get_after_answer_by_trigger(
    trigger: str,
    structure: list[tuple[str]],
) -> str:
    """Возвращает соответствующий направляющий вопрос.

    Args:
        trigger: Триггер действия.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_com_ans in structure:
        if trig_com_ans[1] == trigger:
            return trig_com_ans[4]
    return ""


def get_answer_by_trigger(
    trigger: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующий ответ.

    Args:
        trigger: Триггер действия.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_com_ans in structure:
        if trig_com_ans[1] == trigger:
            return trig_com_ans[3]
    return ""


def get_triggers_group_by_trigger(
    trigger: str,
    structure: list[tuple[str]],
) -> tuple[str] | None:
    """Получаем группу триггеров.

    Необходимо для пропуска сразу целого раздела, в случае отказа пользователя.

    Args:
        trigger: Триггер.
        structure: Структура.

    Returns:
        Группа триггеров.
    """
    for group_triggers in structure:
        if trigger in group_triggers:
            return group_triggers
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


def disagree_answer_by_trigger(
    trigger: str,
    structure: list[tuple[str]],
):
    """Возвращает соответствующий ответ.

    Args:
        trigger: Триггер действия.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_com_ans in structure:
        if trig_com_ans[1] == trigger:
            return trig_com_ans[5]
    return ""


def check_api(data: BaseModel) -> None:
    try:
        data.request.get("command")
        data.request.get("nlu")
        data.session.get("new")
        data.state.get("session")
    except AttributeError:
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
    return f"{answer} {after_answer}"
