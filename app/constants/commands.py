class Commands:
    """Класс для хранения команд пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    about_training_center = (
        "прослушать информацию об учебно-кинологическим "
        "центре собаки-помощники"
    )
    about_staff_1 = "прослушать информацию о персонале центра"
    about_staff_2 = "прослушать информацию о персонале центра продолжение"
    about_staff_3 = "прослушать информацию о персонале центра продолжение 2"
    about_facility = "прослушать описание помещения центра"
    about_training_course = "прослушать информацию о курсе обучения"
    take_manual_training = "пройти обучение по методичке"
    take_quiz = "пройти викторину"
    listen_quiz_results = "узнать результаты викторины"
    listen_to_legislation = "прослушать выдержки из законодательства"
    about_legislation_accessibility = (
        "прослушать информацию о основаниях для доступа к "
        "объектам инфраструктуры"
    )
    about_guide_dog_transportation = "прослушать информацию о провозе собак"
    self_defense_phrase = "прослушать фразу для самозащиты"

    about_discounts_and_free_services = (
        "узнать о скидках/льготах и бесплатных услугах"
    )
    discounts_for_food = "узнать о скидках для питания"
    discounts_for_delicacy = "узнать о скидках на лакомства"
    special_offers_for_veterinaries = (
        "узнать о компенсации расходов на ветеринарию"
    )
    exit_discounts_and_free_services = "выход из скидок и бесплатных услуг"

    about_support_services_for_blind_passengers = (
        "узнать о службах поддержки незрячих пассажиров на транспорте"
    )

    about_services_uniting_blind_people = (
        "узнать о службах объединяющие незрячих"
    )
    about_regional_clubs = "послушать о региональных клубах"
    about_special_view_foundation = "узнать о фонде особый взгляд"
    exit_services_for_blind = "выход из служб поддержки незрячих"

    instructions_for_launching_podcast = (
        "узнать инструкцию запуска подкаста " "министерства наших собачьих дел"
    )

    help_main = "помощь"
    help_phrase = "помощь по фразам"
    help_navigation = "помощь по навигации"
    start = "начинай"
    agree = "да"
    not_agree = "нет"
    exit = "выход"
    next = "дальше"
    repeat = "повтори"


# COMMANDS_TRIGGERS_GET_FUNC_ANSWERS = [
#     (
#         getattr(Commands, command_name),
#         create_trigger(name=command_name),
#         create_func(name=command_name),
#         answers_documents.get(command_name),
#     )
#     for command_name in STATES
# ]

# class Triggers:
#     """Класс для хранения триггеров.
#
#     Триггеры - команды, которые запускают некоторые команды и могут
#     изменять состояние `state`.
#     """
#
#     def __setattr__(self, key, value):
#         raise AttributeError("Триггеры изменять нельзя!")
#
#     ABOUT_TRAINING_CENTER = "trigger_training_center"
#     ABOUT_STAFF = "trigger_staff"
#     ABOUT_ACCOMMODATION = "trigger_accommodation"
#     ABOUT_FACILITY = "trigger_facility"
#     TAKE_TRAINING = "trigger_training"
#     TAKE_QUIZ = "trigger_quiz"
#
#     LISTEN_TO_LEGISLATION = "trigger_legislation"
#     ABOUT_ACCESSIBILITY = "trigger_accessibility"
#     ABOUT_GUIDE_DOG_TRANSPORTATION = "trigger_guide_dog_transportation"
#     SELF_DEFENSE_PHRASE = "trigger_self_defense"
#     EXIT_FROM_LEGISLATION = "trigger_legislation_exit"
#
#     ABOUT_DISCOUNTS_AND_FREE_SERVICES = "trigger_discounts_free_services"
#     DISCOUNTS_FOR_FOOD = "trigger_food"
#     DISCOUNTS_FOR_DELICACY = "trigger_delicacy"
#     SPECIAL_OFFERS_FOR_VETERINARIES = "trigger_veterinaries"
#     EXIT_DISCOUNTS_AND_FREE_SERVICES = "trigger_discounts_free_services_exit"
#
#     ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
#         "trigger_support_services_blind"
#     )
#
#     ABOUT_SERVICES_UNITING_BLIND_PEOPLE = "trigger_services_for_blind"
#     ABOUT_REGIONAL_CLUBS = "trigger_regional_clubs"
#     ABOUT_SPECIAL_VIEW_FOUNDATION = "trigger_special_view_foundation"
#     EXIT_SERVICES_FOR_BLIND = "trigger_services_for_blind_exit"
#
#     INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "trigger_launch_podcast"
#
#     HELP = "trigger_help"
#     HELP_PHRASE = "trigger_help_phrase"
#     HELP_NAVIGATION = "trigger_help_navigation"
#     HELP_EXIT = "trigger_help_exit"
#     EXIT = "trigger_exit"
#
#     NEXT = "trigger_next"
#
#
# class GetFunc:
#     """Класс для хранения имен функций.
#
#     Эти функции после запуска соответствующего триггера. Имена функций
#     и соответвующего триггера отличаются префиксами `get_` и `trigger_`.
#     """
#
#     def __setattr__(self, key, value):
#         raise AttributeError("Команды изменять нельзя!")
#
#     ABOUT_TRAINING_CENTER = "get_training_center"
#     ABOUT_STAFF = "get_staff"
#     ABOUT_ACCOMMODATION = "get_accommodation"
#     ABOUT_FACILITY = "get_facility"
#     TAKE_TRAINING = "get_training"
#     TAKE_QUIZ = "get_quiz"
#
#     LISTEN_TO_LEGISLATION = "get_legislation"
#     ABOUT_ACCESSIBILITY = "get_accessibility"
#     ABOUT_GUIDE_DOG_TRANSPORTATION = "get_guide_dog_transportation"
#     SELF_DEFENSE_PHRASE = "get_self_defense"
#     EXIT_FROM_LEGISLATION = "get_legislation_exit"
#
#     ABOUT_DISCOUNTS_AND_FREE_SERVICES = "get_discounts_free_services"
#     DISCOUNTS_FOR_FOOD = "get_food"
#     DISCOUNTS_FOR_DELICACY = "get_delicacy"
#     SPECIAL_OFFERS_FOR_VETERINARIES = "get_veterinaries"
#     EXIT_DISCOUNTS_AND_FREE_SERVICES = "get_discounts_free_services_exit"
#
#     ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = "get_support_services_blind"
#
#     ABOUT_SERVICES_UNITING_BLIND_PEOPLE = "get_services_for_blind"
#     ABOUT_REGIONAL_CLUBS = "get_regional_clubs"
#     ABOUT_SPECIAL_VIEW_FOUNDATION = "get_special_view_foundation"
#     EXIT_SERVICES_FOR_BLIND = "get_services_for_blind_exit"
#
#     INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "get_launch_podcast"
#
#     HELP = "get_help"
#     HELP_PHRASE = "get_help_phrase"
#     HELP_NAVIGATION = "get_help_navigation"
#     EXIT = "get_exit"
#     NEXT = "get_next"


# class TrigComAns:
#     """Класс для хранения структуры данных.
#
#     Состоит из соответствующих команд, триггеров, функций и ответов.
#
#     Note: для удобства использования в коде.
#     """
#
#     def setattr(self, key, value):
#         raise AttributeError("Команды изменять нельзя!")

# COMMAND_NAMES = [
#     "ABOUT_TRAINING_CENTER",
#     "ABOUT_STAFF",
#     "ABOUT_ACCOMMODATION",
#     "ABOUT_FACILITY",
#     "TAKE_TRAINING",
#     "TAKE_QUIZ",
#     "LISTEN_TO_LEGISLATION",
#     "ABOUT_ACCESSIBILITY",
#     "ABOUT_GUIDE_DOG_TRANSPORTATION",
#     "SELF_DEFENSE_PHRASE",
#     "EXIT_FROM_LEGISLATION",
#     "ABOUT_DISCOUNTS_AND_FREE_SERVICES",
#     "DISCOUNTS_FOR_FOOD",
#     "DISCOUNTS_FOR_DELICACY",
#     "SPECIAL_OFFERS_FOR_VETERINARIES",
#     "EXIT_DISCOUNTS_AND_FREE_SERVICES",
#     "ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS",
#     "ABOUT_SERVICES_UNITING_BLIND_PEOPLE",
#     "ABOUT_REGIONAL_CLUBS",
#     "ABOUT_SPECIAL_VIEW_FOUNDATION",
#     "EXIT_SERVICES_FOR_BLIND",
#     "INSTRUCTIONS_FOR_LAUNCHING_PODCAST",
# ]


# print(TrigComAns.COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)

#
# TRIGGER_ORDER = ["trigger_" + key for key in Answers.ORDER_KEY]
#
# FUNC_BY_ORDER = ["get_" + key for key in Answers.ORDER_KEY]
