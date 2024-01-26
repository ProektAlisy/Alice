from app.constants.commands_triggers_functions import TrigComAns
from app.command_classes import Commands


def is_completed(progress: list[str]) -> bool:
    """Проверяет, завершено ли обучение.

    Обучение считается завершенным, когда выполенные все элементы навыка.

    Args:
        progress: Список прогресса выполнения. В него входят триггеры,
        соответствующие выполненным элементам навыка.

    Returns:
        True, если все элементы навыка завершены, иначе False.
    """
    return len(get_triggers_by_order()) == len(progress)


def get_next_trigger(progress: list[str]) -> str:
    """Возвращает следующий триггер.

    Очередность определяется списком TrigComAns.COMMANDS_NAMES.

    Args:
        progress: Список прогресса выполнения.

    Returns:
        Следующий триггер.
    """
    trigger = progress[-1]
    ordered_triggers = get_triggers_by_order()
    trigger_index = ordered_triggers.index(trigger)
    len_triggers = len(ordered_triggers)
    for index in range(trigger_index, len_triggers + trigger_index):
        if ordered_triggers[index % len_triggers] in progress:
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


def get_all_commands() -> list[str]:
    """
    Возвращает список всех команд из класса Commands.
    """
    return [value for name, value in vars(Commands).items()
            if not name.startswith('__')]
