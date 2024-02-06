from typing import Final

STATES: Final = [
    "start",
    "about_training_center",
    "about_facility",
    "about_staff_1",
    "about_staff_2",
    "about_staff_3",
    "about_training_course",
    "take_manual_training",
    "take_quiz",
    "listen_quiz_results",
    "listen_to_legislation",
    "about_legislation_accessibility",
    "about_guide_dog_transportation",
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
]
DISAGREE_STATES: Final = [state + "_disagree" for state in STATES]

TRIGGERS_BY_GROUP: Final = [
    ("trigger_about_training_center",),
    ("trigger_about_facility",),
    (
        "about_staff_1",
        "about_staff_2",
        "about_staff_3",
    ),
    ("trigger_about_training_course",),
    ("trigger_take_manual_training",),
    (
        "trigger_take_quiz",
        "trigger_listen_quiz_results",
    ),
    (
        "trigger_listen_to_legislation",
        "trigger_about_legislation_accessibility",
        "trigger_about_guide_dog_transportation",
        "trigger_about_transportation_by_land_transport",
        "trigger_about_transportation_by_rail",
        "trigger_about_air_transportation",
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
    "about_staff_1",
    "trigger_take_quiz",
    "trigger_listen_to_legislation",
    "trigger_about_discounts_and_free_services",
    "trigger_about_services_uniting_blind_people",
    "trigger_about_podcast",
]
