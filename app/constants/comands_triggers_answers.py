from app.constants.commands import Commands
from app.constants.states import STATES
from app.monga_initialize import connect_to_mongodb
from app.utils import (
    create_trigger,
    create_func,
    read_from_db,
)


(
    db,
    answers_collection,
    after_answers_collection,
    disagree_answers_collection,
) = connect_to_mongodb()

answers_documents = read_from_db(answers_collection)
after_answers_documents = read_from_db(after_answers_collection)
disagree_answers_documents = read_from_db(disagree_answers_collection)


COMMANDS_TRIGGERS_GET_FUNC_ANSWERS = [
    (
        getattr(Commands, command_name),
        create_trigger(name=command_name),
        create_func(name=command_name),
        answers_documents.get(command_name, ""),
        after_answers_documents.get(command_name, ""),
        disagree_answers_documents.get(command_name, ""),
    )
    for command_name in STATES
]
