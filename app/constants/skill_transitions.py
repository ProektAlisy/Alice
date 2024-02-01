"""
Хранятся описания переходов между состояниями и соответствующих действиях.
"""
import itertools

from app.constants.states import DISAGREE_STATES, STATES
from app.utils import create_func, create_trigger

transitions = [
    [
        # переходы из состояния согласия к следующему состоянию согласия
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": state,
            "dest": STATES[number + 1],
            "before": create_func(STATES[number + 1]),
            "conditions": "is_agree",
        },
        # переход из состояния согласия в состояние отказа
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": state,
            "dest": "=",
            "before": create_func(DISAGREE_STATES[number + 1]),
            "conditions": "is_disagree",
        },
        # переход из любого состояния в состояние отказа
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": "*",
            "dest": "=",
            "before": create_func(DISAGREE_STATES[number + 1]),
            "conditions": "is_disagree",
        },
        # переход из состояния с отказом в состояние согласия
        {
            "trigger": create_trigger(STATES[number + 1]),
            "source": "*",
            "dest": state,
            "before": create_func(STATES[number + 1]),
            "conditions": "is_agree",
        },
        # безусловный переход из любого состояния в любое
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
