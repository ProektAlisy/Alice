from typing import Final

QUIZ_STATE: Final = "take_quiz"
MANUAL_TRAINING_STATE: Final = "take_manual_training"
HELP_STATE: Final = "help_main"
STATES: Final = [
    "start",
    "about_training_center",
    "about_facility",
    "about_staff_1",
    "about_staff_2",
    "about_staff_3",
    "about_training_course",
    MANUAL_TRAINING_STATE,
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
QUIZ_TRIGGER_STATE: Final = QUIZ_STATE
STATE_HELP_MAIN = HELP_STATE
DISAGREE_STATES: Final = [state + "_disagree" for state in STATES]
POSSIBILITIES_TRIGGER: Final = "possibilities"
STATES_BY_GROUP: Final = [
    ("about_training_center",),
    ("about_facility",),
    (
        "about_staff_1",
        "about_staff_2",
        "about_staff_3",
    ),
    ("about_training_course",),
    (MANUAL_TRAINING_STATE,),
    (QUIZ_TRIGGER_STATE,),
    (
        "listen_to_legislation",
        "about_legislation_accessibility",
        "about_transportation_by_land_transport",
        "about_transportation_by_rail",
        "about_transportation_by_air",
        "about_transportation_by_water",
        "self_defense_phrase",
    ),
    ("about_support_services_for_blind_passengers",),
    (
        "about_discounts_and_free_services",
        "discounts_for_food",
        "discounts_for_delicacy",
        "special_offers_for_veterinaries",
    ),
    (
        "about_services_uniting_blind_people",
        "about_regional_clubs",
        "about_special_view_foundation",
    ),
    (
        "about_podcast",
        "tinstructions_for_launching_podcast",
    ),
]
CORE_STATES: Final = [
    "about_staff_1",
    "listen_to_legislation",
    "about_discounts_and_free_services",
    "about_services_uniting_blind_people",
    "about_podcast",
]
