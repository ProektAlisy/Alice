from typing import Final

QUIZ_STATE: Final = "take_quiz"
STATES: Final = [
    "start",
    "about_training_center",
    "about_facility",
    "about_staff_1",
    "about_staff_2",
    "about_staff_3",
    "about_training_course",
    "take_manual_training",
    QUIZ_STATE,
    "listen_to_legislation",
    "about_legislation_accessibility",
    "about_transportation_by_land_transport",
    "about_transportation_by_rail",
    "about_air_transportation",
    "about_transportation_by_water",
    "self_defense_phrase",
    "about_support_services_for_blind_passengers",
    "about_discounts_and_free_services",
    "discounts_for_food",
    "discounts_for_delicacy",
    "special_offers_for_veterinaries",
    "about_services_uniting_blind_people",
    "about_regional_clubs",
    "about_special_view_foundation",
    "about_podcast",
    "instructions_for_launching_podcast",
]
HELP_STATES: Final = [
    "help_main",
    "possibilities",
    "help_phrase",
    "useful_information",
]
QUIZ_TRIGGER_STATE: Final = "trigger_" + QUIZ_STATE

DISAGREE_STATES: Final = [state + "_disagree" for state in STATES]
POSSIBILITIES_TRIGGER: Final = "trigger_possibilities"
TRIGGERS_BY_GROUP: Final = [
    ("trigger_about_training_center",),
    ("trigger_about_facility",),
    (
        "trigger_about_staff_1",
        "trigger_about_staff_2",
        "trigger_about_staff_3",
    ),
    ("trigger_about_training_course",),
    ("trigger_take_manual_training",),
    (QUIZ_TRIGGER_STATE,),
    (
        "trigger_listen_to_legislation",
        "trigger_about_legislation_accessibility",
        "trigger_about_transportation_by_land_transport",
        "trigger_about_transportation_by_rail",
        "trigger_about_transportation_by_air",
        "trigger_about_transportation_by_water",
        "trigger_self_defense_phrase",
    ),
    ("trigger_about_support_services_for_blind_passengers",),
    (
        "trigger_about_discounts_and_free_services",
        "trigger_discounts_for_food",
        "trigger_discounts_for_delicacy",
        "trigger_special_offers_for_veterinaries",
    ),
    (
        "trigger_about_services_uniting_blind_people",
        "trigger_about_regional_clubs",
        "trigger_about_special_view_foundation",
    ),
    (
        "trigger_about_podcast",
        "trigger_instructions_for_launching_podcast",
    ),
]
CORE_TRIGGERS: Final = [
    "trigger_about_staff_1",
    "trigger_listen_to_legislation",
    "trigger_about_discounts_and_free_services",
    "trigger_about_services_uniting_blind_people",
    "trigger_about_podcast",
]
