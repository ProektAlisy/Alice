"""
Хранятся описания переходов между состояниями и соответствующих действиях.
"""
import itertools

from app.constants.states import STATES, DISAGREE_STATES
from app.utils import (
    create_trigger,
    create_func_study,
    create_func,
)

transitions = [
    [
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": state,
            "dest": STATES[number + 1],
            "before": create_func(STATES[number + 1]),
            "conditions": "is_agree",
        },
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": state,
            "dest": DISAGREE_STATES[number + 1],
            "before": create_func(DISAGREE_STATES[number + 1]),
            "conditions": "is_disagree",
        },
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": "*",
            "dest": "=",
            "before": create_func(STATES[number + 1]),
        },
    ]
    for number, state in enumerate(STATES)
    if number != len(STATES) - 1
]
TRANSITIONS = list(itertools.chain.from_iterable(transitions))
print(TRANSITIONS)
