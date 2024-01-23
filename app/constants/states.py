"""
Хранятся описания переходов между состояниями и соответствующих действиях.
"""

from app.constants.commands_triggers_functions import GetFunc, Triggers

TRANSITIONS = [
    {
        "trigger": Triggers.ABOUT_TRAINING_CENTER,
        "source": "start",
        "dest": "=",
        "before": GetFunc.ABOUT_TRAINING_CENTER,
    },
    {
        "trigger": Triggers.ABOUT_STAFF,
        "source": "start",
        "dest": "=",
        "before": GetFunc.ABOUT_STAFF,
    },
    {
        "trigger": Triggers.ABOUT_ACCOMMODATION,
        "source": "start",
        "dest": "=",
        "before": GetFunc.ABOUT_ACCOMMODATION,
    },
    {
        "trigger": Triggers.ABOUT_FACILITY,
        "source": "start",
        "dest": "=",
        "before": GetFunc.ABOUT_FACILITY,
    },
    {
        "trigger": Triggers.TAKE_TRAINING,
        "source": "start",
        "dest": "start",
        "before": GetFunc.TAKE_TRAINING,
    },
    {
        "trigger": Triggers.TAKE_QUIZ,
        "source": "start",
        "dest": "start",
        "before": GetFunc.TAKE_QUIZ,
    },
    {
        "trigger": Triggers.LISTEN_TO_LEGISLATION,
        "source": "start",
        "dest": "legislation",
        "before": GetFunc.LISTEN_TO_LEGISLATION,
    },
    {
        "trigger": Triggers.ABOUT_ACCESSIBILITY,
        "source": "legislation",
        "dest": "legislation",
        "before": GetFunc.ABOUT_ACCESSIBILITY,
    },
    {
        "trigger": Triggers.ABOUT_GUIDE_DOG_TRANSPORTATION,
        "source": "legislation",
        "dest": "legislation",
        "before": GetFunc.ABOUT_GUIDE_DOG_TRANSPORTATION,
    },
    {
        "trigger": Triggers.SELF_DEFENSE_PHRASE,
        "source": "legislation",
        "dest": "legislation",
        "before": GetFunc.SELF_DEFENSE_PHRASE,
    },
    {
        "trigger": Triggers.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
        "source": "start",
        "dest": "discounts_free_services",
        "before": GetFunc.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
    },
    {
        "trigger": Triggers.DISCOUNTS_FOR_FOOD,
        "source": "discounts_free_services",
        "dest": "discounts_free_services",
        "before": GetFunc.DISCOUNTS_FOR_FOOD,
    },
    {
        "trigger": Triggers.DISCOUNTS_FOR_DELICACY,
        "source": "discounts_free_services",
        "dest": "discounts_free_services",
        "before": GetFunc.DISCOUNTS_FOR_DELICACY,
    },
    {
        "trigger": Triggers.SPECIAL_OFFERS_FOR_VETERINARIES,
        "source": "discounts_free_services",
        "dest": "discounts_free_services",
        "before": GetFunc.SPECIAL_OFFERS_FOR_VETERINARIES,
    },
    {
        "trigger": Triggers.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
        "source": "start",
        "dest": "=",
        "before": GetFunc.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
    },
    {
        "trigger": Triggers.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
        "source": "start",
        "dest": "=",
        "before": GetFunc.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
    },
    {
        "trigger": Triggers.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
        "source": "start",
        "dest": "services_for_blind",
        "before": GetFunc.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
    },
    {
        "trigger": Triggers.ABOUT_REGIONAL_CLUBS,
        "source": "services_for_blind",
        "dest": "services_for_blind",
        "before": GetFunc.ABOUT_REGIONAL_CLUBS,
    },
    {
        "trigger": Triggers.ABOUT_SPECIAL_VIEW_FOUNDATION,
        "source": "services_for_blind",
        "dest": "services_for_blind",
        "before": GetFunc.ABOUT_SPECIAL_VIEW_FOUNDATION,
    },
    {
        "trigger": Triggers.HELP,
        "source": "*",
        "dest": "help",
        "before": GetFunc.HELP,
    },
    {
        "trigger": Triggers.HELP_PHRASE,
        "source": "help",
        "dest": "help",
        "before": GetFunc.HELP_PHRASE,
    },
    {
        "trigger": Triggers.HELP_NAVIGATION,
        "source": "help",
        "dest": "help",
        "before": GetFunc.HELP_NAVIGATION,
    },
    {
        "trigger": Triggers.HELP_EXIT,
        "source": "help",
        "dest": "=",
        "before": GetFunc.HELP_EXIT,
        "after": "_return_to_original_state",
    },
    {
        "trigger": Triggers.EXIT_FROM_LEGISLATION,
        "source": "legislation",
        "dest": "=",
        "before": GetFunc.EXIT_FROM_LEGISLATION,
        "after": "_return_to_original_state",
    },
    {
        "trigger": Triggers.EXIT_DISCOUNTS_AND_FREE_SERVICES,
        "source": "discounts_free_services",
        "dest": "=",
        "before": GetFunc.EXIT_DISCOUNTS_AND_FREE_SERVICES,
        "after": "_return_to_original_state",
    },
    {
        "trigger": Triggers.EXIT_SERVICES_FOR_BLIND,
        "source": "services_for_blind",
        "dest": "=",
        "before": GetFunc.EXIT_SERVICES_FOR_BLIND,
        "after": "_return_to_original_state",
    },
]
