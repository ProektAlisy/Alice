from app.constants.commands_triggers_functions import TrigComAns
from app.monga_initialize import db


def is_completed(skill: "FiniteStateMachine") -> bool: # noqa
    """Проверяет, завершено ли обучение.

    Обучение считается завершенным, когда выполенные все элементы навыка.

    Args:
        skill: объект навыка.

    Returns:
        True, если все элементы навыка завершены, иначе False.
    """
    try:
        result = len(skill.progress) == skill.max_progress
    except TypeError:
        result = False
    return result


def get_next_trigger(skill: "FiniteStateMachine") -> str: # noqa
    """Возвращает следующий триггер.

    Очередность определяется списком TrigComAns.COMMANDS_NAMES.

    Args:
        skill: Объект навыка.

    Returns:
        Следующий триггер.
    """
    trigger = last_trigger(skill)
    if last_trigger(skill) is None:
        return TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS[0][1]
    ordered_triggers = get_triggers_by_order()
    trigger_index = ordered_triggers.index(trigger)
    len_triggers = len(ordered_triggers)
    for index in range(trigger_index, len_triggers + trigger_index):
        if ordered_triggers[index % len_triggers] in skill.progress:
            continue
        return ordered_triggers[index % len_triggers]


def get_trigger_by_command(command: str) -> str | None:
    """Возвращает триггер, соответствующий заданной команде.

    Args:
        command: Команда.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        if trig_commands[0] == command:
            return trig_commands[1]
    return None


def get_triggers_by_order() -> list[str]:
    """Возвращает список триггеров.

    Порядок определяется по соответствию триггеру команде из списка
    TrigComAns.COMMANDS_NAMES.

    Returns:
        Список триггеров.
    """
    triggers = []
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        triggers.append(trig_commands[1])
    return triggers


def get_func_answers_command() -> list[tuple[str, str, str]]:
    """
    Возвращает команды без соответствующих триггеров.

    Returns:
        Список кортежей (Триггер, Функция, Ответ).
    """
    commands_without_triggers = []
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        command_tuple = (trig_commands[2], trig_commands[3], trig_commands[0])
        commands_without_triggers.append(command_tuple)
    return commands_without_triggers


def get_all_commands() -> list[str]:
    """Возвращает список команд.

    Returns:
        Список команд.
    """
    commands = []
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        commands.append(trig_commands[0])
    return commands


def transform_string(input_string: str) -> str:
    """Преобразует строку.

    Из snake_case в CamelCase. Используется для генерации имен классов.

    Args:
        input_string: Входная строка.

    Returns:
        Преобразованная строка.
    """
    parts = input_string.split("_")
    transformed_parts = [part.capitalize() for part in parts]
    return "".join(transformed_parts) + "Command"


def is_alice_commands(command: str) -> bool:
    with open(
        "app/constants/alice_commands.txt",
        "r",
        encoding="utf-8",
    ) as file:
        commands = [line.strip() for line in file]
    return command in commands


def last_trigger(skill) -> str:
    """Возвращает последний триггер.

    Args:
        skill: Объект навыка.

    Returns:
        Последний триггер.
    """
    try:
        result = skill.progress[-1]
    except (IndexError, TypeError):
        result = None
    return result


def read_from_db(query, collection):
    # print(db[collection].find_one(query, {"_id": 0}))
    return db[collection].find_one(query, {"_id": 0})
