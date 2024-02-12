from app.constants.commands import Commands
from app.constants.intents import Intents
from app.constants.states import HELP_STATES, STATES
from app.monga.monga_initialize import (
    after_answers_collection,
    answers_collection,
    disagree_answers_collection,
)
from app.core.utils import (
    create_func,
    create_trigger,
    get_triggers_by_order,
    read_from_db,
)

answers_documents = read_from_db(answers_collection)
after_answers_documents = read_from_db(after_answers_collection)
disagree_answers_documents = read_from_db(disagree_answers_collection)

COMMANDS_TRIGGERS_GET_FUNC_ANSWERS = [
    (
        getattr(Commands, command_name.upper()),
        create_trigger(command_name),
        create_func(command_name),
        answers_documents.get(command_name, ""),
        after_answers_documents.get(command_name, ""),
        disagree_answers_documents.get(command_name, ""),
        getattr(Intents, command_name.upper()),
    )
    for command_name in STATES[1:] + HELP_STATES
]

ORDERED_TRIGGERS = get_triggers_by_order(COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)
