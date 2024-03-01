from icecream import ic

from app.constants.comands_states_answers import (
    answers_documents,
    after_answers_documents,
    COMMANDS_STATES_ANSWERS_INTENTS,
)
from app.constants.states import HELP_STATES
from app.core.utils import get_state_by_answer, get_state_by_after_answer


num_of_errors = 0
for answer in answers_documents.values():
    if get_state_by_answer(
        answer,
        COMMANDS_STATES_ANSWERS_INTENTS,
    ) in HELP_STATES[:-1] + [
        "take_quiz",
    ]:
        continue
    for after_answer in after_answers_documents.values():
        if len(after_answer) + len(answer) > 1024:
            num_of_errors += 1
            bad_after_answer = get_state_by_after_answer(
                after_answer,
                COMMANDS_STATES_ANSWERS_INTENTS,
            )
            bad_answer = get_state_by_answer(
                answer,
                COMMANDS_STATES_ANSWERS_INTENTS,
            )
            print(
                f"_________________\nanswer:  {bad_answer}",
                f"\nafter_answer: {bad_after_answer}",
                f"\nПревышение  на: {len(after_answer) + len(answer) - 1009}",
            )
ic(f"Число превышений 1024 символа: {num_of_errors}")
