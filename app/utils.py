from app.constants.user_commands import TrigComAns


def get_command_by_trigger(trigger):
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        if trig_commands[1] == trigger:
            return trig_commands[2]
    return None


def get_trigger_by_command(command):
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        if trig_commands[0] == command:
            return trig_commands[1]
    return None


def get_first_elements():
    first_elements = []
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        first_elements.append(trig_commands[0])
    return first_elements


def get_func_answers_command():
    commands_without_triggers = []
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        command_tuple = (trig_commands[2], trig_commands[3], trig_commands[0])
        commands_without_triggers.append(command_tuple)
    return commands_without_triggers
