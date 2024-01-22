from app.constants.commands_triggers_functions import TrigComAns


def get_command_by_trigger(trigger):
    """
    Return the command associated with the given trigger
    from the TRIGGERS_COMMANDS_ANSWERS array.
    """
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        if trig_commands[1] == trigger:
            return trig_commands[2]
    return None


def get_trigger_by_command(command):
    """
    Function to retrieve trigger by command
    from TrigComAns.TRIGGERS_COMMANDS_ANSWERS.
    """
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        if trig_commands[0] == command:
            return trig_commands[1]
    return None


def get_first_elements():
    """
    Get the first elements
    from TrigComAns.TRIGGERS_COMMANDS_ANSWERS and return them as a list.
    """
    first_elements = []
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        first_elements.append(trig_commands[0])
    return first_elements


def get_func_answers_command():
    """
    Retrieves the command answers without triggers
    from TrigComAns.TRIGGERS_COMMANDS_ANSWERS
    and returns them as a list of tuples containing three elements each.
    """
    commands_without_triggers = []
    for trig_commands in TrigComAns.TRIGGERS_COMMANDS_ANSWERS:
        command_tuple = (trig_commands[2], trig_commands[3], trig_commands[0])
        commands_without_triggers.append(command_tuple)
    return commands_without_triggers
