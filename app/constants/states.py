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
    "self_defense_phrase",
    "about_legislation_accessibility",
    "about_guide_dog_transportation",
]
HELP_STATES: Final = [
    "help_main",
    "possibilities",
    "help_phrase",
]
DISAGREE_STATES: Final = [state + "_disagree" for state in STATES]
