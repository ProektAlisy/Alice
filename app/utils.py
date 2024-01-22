from app.constants.commands_triggers_functions import TrigComAns


def is_completed(progress: list[str]):
    return len(get_triggers_by_order()) == len(progress)


def get_next_trigger(progress):
    trigger = progress[-1]
    ordered_triggers = get_triggers_by_order()
    trigger_index = ordered_triggers.index(trigger)
    len_triggers = len(ordered_triggers)
    for index in range(trigger_index, len_triggers + trigger_index):
        if ordered_triggers[index % len_triggers] in progress:
            continue
        return ordered_triggers[index % len_triggers]


def get_trigger_by_command(command):
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        if trig_commands[0] == command:
            return trig_commands[1]
    return None


def get_triggers_by_order() -> list[str]:
    triggers = []
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        triggers.append(trig_commands[1])
    return triggers


def get_func_answers_command():
    commands_without_triggers = []
    for trig_commands in TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS:
        command_tuple = (trig_commands[2], trig_commands[3], trig_commands[0])
        commands_without_triggers.append(command_tuple)
    return commands_without_triggers
