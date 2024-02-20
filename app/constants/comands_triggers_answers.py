from app.constants.commands import Commands
from app.constants.intents import INTENTS
from app.constants.states import HELP_STATES, STATES
from app.core.utils import (
    create_func,
    get_triggers_by_order,
    read_from_db,
)
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

COMMANDS_STATES_GET_FUNC_ANSWERS = [
    (
        getattr(Commands, state.upper()),
        state,
        create_func(state),
        answers_documents.get(state, ""),
        after_answers_documents.get(state, ""),
        disagree_answers_documents.get(state, ""),
        getattr(INTENTS, state.upper()),
    )
    for state in STATES[1:] + HELP_STATES
]

ORDERED_STATES = get_triggers_by_order(COMMANDS_STATES_GET_FUNC_ANSWERS)
