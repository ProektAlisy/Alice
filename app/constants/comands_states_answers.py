from app.constants.commands import Commands, HelpCommands
from app.constants.intents import INTENTS
from app.constants.states import HELP_STATES, STATES
from app.core.utils import get_all_commands, get_states_by_order, read_from_db
from app.monga.monga_initialize import (
    after_answers_collection,
    another_answers_collection,
    answers_collection,
    disagree_answers_collection,
)

answers_documents = read_from_db(answers_collection)
after_answers_documents = read_from_db(after_answers_collection)
disagree_answers_documents = read_from_db(disagree_answers_collection)
another_answers_documents = read_from_db(another_answers_collection)

COMMANDS_STATES_ANSWERS_INTENTS = [
    (
        getattr(Commands, state.upper()),
        state,
        answers_documents.get(state, ""),
        after_answers_documents.get(state, ""),
        disagree_answers_documents.get(state, ""),
        getattr(INTENTS, state.upper()),
    )
    for state in STATES[1:]
]

ALL_COMMANDS = get_all_commands(COMMANDS_STATES_ANSWERS_INTENTS)

HELP_COMMANDS_STATES_ANSWERS_INTENTS = [
    (
        getattr(HelpCommands, state.upper()),
        state,
        answers_documents.get(state, ""),
        after_answers_documents.get(state, ""),
        disagree_answers_documents.get(state, ""),
        getattr(INTENTS, state.upper()),
    )
    for state in HELP_STATES
]
HELP_COMMANDS = get_all_commands(HELP_COMMANDS_STATES_ANSWERS_INTENTS)

ORDERED_STATES = get_states_by_order(COMMANDS_STATES_ANSWERS_INTENTS)
