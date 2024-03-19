"""
Вспомогательный скрипт для проверки длин answer и after_answer во всех
различных сочетаниях.
"""
from icecream import ic

from app.constants.comands_states_answers import (
    COMMANDS_STATES_ANSWERS_INTENTS,
    after_answers_documents,
    answers_documents,
    HELP_COMMANDS_STATES_ANSWERS_INTENTS,
)
from app.constants.states import HELP_STATES
from app.core.utils import get_state_by_answer, get_state_by_after_answer


exclude_states = HELP_STATES + ["take_quiz", "take_manual_training"]
num_of_errors = 0
for answer in answers_documents.values():
    if (
        get_state_by_answer(
            answer,
            HELP_COMMANDS_STATES_ANSWERS_INTENTS,
        )
        in exclude_states
    ):
        continue
    for after_answer in after_answers_documents.values():
        if len(after_answer) + len(answer) > 1024:
            num_of_errors += 1
            print(
                f"____________________\nanswer_filename: ",
                f"{get_state_by_answer(answer, COMMANDS_STATES_ANSWERS_INTENTS)}",
                f"\nanswer:  {answer}",
                "\nafter_answer_filename:",
                f"{get_state_by_after_answer(after_answer, COMMANDS_STATES_ANSWERS_INTENTS)}",
                f"\nafter_answer: {after_answer}",
                f"\nПревышение  на: {len(after_answer) + len(answer) - 1009}",
            )
ic(f"Число превышений 1024 символа: {num_of_errors}")
