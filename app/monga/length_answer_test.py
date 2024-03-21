from icecream import ic

from app.constants.comands_states_answers import (
    HELP_COMMANDS_STATES_ANSWERS_INTENTS,
    after_answers_documents,
    answers_documents,
)
from app.constants.states import HELP_STATES
from app.core.utils import get_state_by_answer

num_of_errors = 0
for answer in answers_documents.values():
    if get_state_by_answer(
        answer,
        HELP_COMMANDS_STATES_ANSWERS_INTENTS,
    ) in HELP_STATES + [
        "take_quiz",
        "take_manual_training",
    ]:
        continue
    for after_answer in after_answers_documents.values():
        if len(after_answer) + len(answer) > 1011:
            num_of_errors += 1
            ic(
                f"_________________\nanswer:  {answer}",
                f"\nafter_answer: {after_answer}",
                f"\nПревышение  на: {len(after_answer) + len(answer) - 1011}",
            )
ic(f"Число превышений 1024 символа: {num_of_errors}")
