from pymongo.collection import Collection


def is_completed(skill: "FiniteStateMachine") -> bool:  # noqa
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


def get_next_trigger(
    skill: "FiniteStateMachine",  # noqa
    triggers: list,
) -> str:
    """Возвращает следующий триггер.

    Очередность определяется списком TrigComAns.COMMANDS_NAMES.

    Args:
        triggers: Список все триггеров.
        skill: Объект навыка.

    Returns:
        Следующий триггер.
    """
    trigger = last_trigger(skill)
    ordered_triggers = get_triggers_by_order(triggers)
    if trigger is None:
        return ordered_triggers[1]

    trigger_index = ordered_triggers.index(trigger)
    len_triggers = len(ordered_triggers)
    for index in range(trigger_index, len_triggers + trigger_index):
        if ordered_triggers[index % len_triggers] in skill.progress:
            continue
        return ordered_triggers[index % len_triggers]


def get_trigger_by_command(command: str, structure: tuple) -> str | None:
    """Возвращает триггер, соответствующий заданной команде.

    Args:
        command: Команда.
        structure: Структура, содержащая соответствующие команды и триггеры.

    Returns:
        Триггер, соответствующий команде. Если соответствующий триггер
        не найден, возвращает None.
    """
    for trig_commands in structure:
        if trig_commands[0] == command:
            return trig_commands[1]
    return None


def get_triggers_by_order(trig_com_ans: list[tuple[str, str]]) -> list[str]:
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


def get_func_answers_command(
    structure: tuple,
) -> list[tuple[str, str, str, str, str]]:
    """
    Возвращает команды без соответствующих триггеров.

    Returns:
        Список кортежей (Триггер, Функция, Ответ).
    """
    commands_without_triggers = []
    for trig_commands in structure:
        command_tuple = (
            trig_commands[2],
            trig_commands[3],
            trig_commands[4],
            trig_commands[5],
            trig_commands[0],
        )
        commands_without_triggers.append(command_tuple)
    return commands_without_triggers


def get_all_commands(structure: tuple) -> list[str]:
    """Возвращает список команд.

    Returns:
        Список команд.
    """
    commands = []
    for trig_commands in structure:
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


def read_from_db(collection: Collection):
    """Читает из БД и преобразует в словарь.

    Args:
        collection: Коллекция в БД.

    Returns:
        Словарь вида {key: answer}
    """
    documents = collection.find({}, projection={"_id": False})
    return {doc["key"]: doc["answer"] for doc in documents}


def create_trigger(name: str) -> str:
    """Создает имя триггера.

    Args:
        name: Имя состояния.

    Returns:
        Имя триггера
    """
    return "trigger_" + name


def create_func(name):
    """Создает имя функции.

    Args:
        name: Имя состояния.

    Returns:
        Имя функции
    """
    return "get_" + name
