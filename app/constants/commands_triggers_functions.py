from app.constants.answers import Answers


class Commands:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    ABOUT_TRAINING_CENTER = "прослушать информацию об учебно-кинологическим центре собаки-помощники"
    ABOUT_STAFF = "прослушать информацию о персонале центра"
    ABOUT_ACCOMMODATION = "прослушать информацию о проживании в центре"
    ABOUT_FACILITY = "прослушать описание помещения центра"
    TAKE_TRAINING = "пройти обучение"
    TAKE_QUIZ = "пройти викторину"

    LISTEN_TO_LEGISLATION = "прослушать выдержки из законодательства"
    ABOUT_ACCESSIBILITY = "прослушать информацию о основаниях для доступа к объектам инфраструктуры"
    ABOUT_GUIDE_DOG_TRANSPORTATION = "прослушать информацию о провозе собак"
    SELF_DEFENSE_PHRASE = "прослушать фразу для самозащиты"
    EXIT_FROM_LEGISLATION = "выход из законодательства"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = (
        "узнать о скидках/льготах и бесплатных услугах"
    )
    DISCOUNTS_FOR_FOOD = "узнать о скидках для питания"
    DISCOUNTS_FOR_DELICACY = "узнать о скидках на лакомства"
    SPECIAL_OFFERS_FOR_VETERINARIES = (
        "узнать о компенсации расходов на ветеринарию"
    )
    EXIT_DISCOUNTS_AND_FREE_SERVICES = "выход из скидок и бесплатных услуг"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "узнать о службах поддержки незрячих пассажиров на транспорте"
    )

    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = (
        "узнать о службах объединяющие незрячих"
    )
    ABOUT_REGIONAL_CLUBS = "послушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "узнать о фонде особый взгляд"
    EXIT_SERVICES_FOR_BLIND = "выход из служб поддержки незрячих"

    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "узнать инструкцию запуска подкаста "
        "министерства наших собачьих дел"
    )

    HELP = "помощь"
    HELP_PHRASE = "помощь по фразам"
    HELP_NAVIGATION = "помощь по навигации"
    HELP_EXIT = "выход из помощи"
    EXIT = "выход"
    NEXT = "следующее"


class Triggers:
    def __setattr__(self, key, value):
        raise AttributeError("Триггеры изменять нельзя!")

    ABOUT_TRAINING_CENTER = "trigger_training_center"
    ABOUT_STAFF = "trigger_staff"
    ABOUT_ACCOMMODATION = "trigger_accommodation"
    ABOUT_FACILITY = "trigger_facility"
    TAKE_TRAINING = "trigger_training"
    TAKE_QUIZ = "trigger_quiz"

    LISTEN_TO_LEGISLATION = "trigger_legislation"
    ABOUT_ACCESSIBILITY = "trigger_accessibility"
    ABOUT_GUIDE_DOG_TRANSPORTATION = "trigger_guide_dog_transportation"
    SELF_DEFENSE_PHRASE = "trigger_self_defense"
    EXIT_FROM_LEGISLATION = "trigger_legislation_exit"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = "trigger_discounts_free_services"
    DISCOUNTS_FOR_FOOD = "trigger_food"
    DISCOUNTS_FOR_DELICACY = "trigger_delicacy"
    SPECIAL_OFFERS_FOR_VETERINARIES = "trigger_veterinaries"
    EXIT_DISCOUNTS_AND_FREE_SERVICES = "trigger_discounts_free_services_exit"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "trigger_support_services_blind"
    )

    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = "trigger_services_for_blind"
    ABOUT_REGIONAL_CLUBS = "trigger_regional_clubs"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "trigger_special_view_foundation"
    EXIT_SERVICES_FOR_BLIND = "trigger_services_for_blind_exit"

    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "trigger_launch_podcast"

    HELP = "trigger_help"
    HELP_PHRASE = "trigger_help_phrase"
    HELP_NAVIGATION = "trigger_help_navigation"
    HELP_EXIT = "trigger_help_exit"
    EXIT = "trigger_exit"

    NEXT = "trigger_next"


class GetFunc:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    ABOUT_TRAINING_CENTER = "get_training_center"
    ABOUT_STAFF = "get_staff"
    ABOUT_ACCOMMODATION = "get_accommodation"
    ABOUT_FACILITY = "get_facility"
    TAKE_TRAINING = "get_training"
    TAKE_QUIZ = "get_quiz"

    LISTEN_TO_LEGISLATION = "get_legislation"
    ABOUT_ACCESSIBILITY = "get_accessibility"
    ABOUT_GUIDE_DOG_TRANSPORTATION = "get_guide_dog_transportation"
    SELF_DEFENSE_PHRASE = "get_self_defense"
    EXIT_FROM_LEGISLATION = "get_legislation_exit"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = "get_discounts_free_services"
    DISCOUNTS_FOR_FOOD = "get_food"
    DISCOUNTS_FOR_DELICACY = "get_delicacy"
    SPECIAL_OFFERS_FOR_VETERINARIES = "get_veterinaries"
    EXIT_DISCOUNTS_AND_FREE_SERVICES = "get_discounts_free_services_exit"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = "get_support_services_blind"

    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = "get_services_for_blind"
    ABOUT_REGIONAL_CLUBS = "get_regional_clubs"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "get_special_view_foundation"
    EXIT_SERVICES_FOR_BLIND = "get_services_for_blind_exit"

    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "get_launch_podcast"

    HELP = "get_help"
    HELP_PHRASE = "get_help_phrase"
    HELP_NAVIGATION = "get_help_navigation"
    HELP_EXIT = "get_help_exit"
    EXIT = "get_exit"
    NEXT = "get_next"

    CORE_COMMANDS = (
        ABOUT_TRAINING_CENTER,
        ABOUT_STAFF,
        ABOUT_ACCOMMODATION,
        ABOUT_FACILITY,
        TAKE_TRAINING,
        TAKE_QUIZ,
        LISTEN_TO_LEGISLATION,
        ABOUT_DISCOUNTS_AND_FREE_SERVICES,
        ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
        INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
    )


class TrigComAns:
    def setattr(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    COMMAND_NAMES = [
        "ABOUT_TRAINING_CENTER",
        "ABOUT_STAFF",
        "ABOUT_ACCOMMODATION",
        "ABOUT_FACILITY",
        "TAKE_TRAINING",
        "TAKE_QUIZ",
        "LISTEN_TO_LEGISLATION",
        "ABOUT_ACCESSIBILITY",
        "ABOUT_GUIDE_DOG_TRANSPORTATION",
        "SELF_DEFENSE_PHRASE",
        "EXIT_FROM_LEGISLATION",
        "ABOUT_DISCOUNTS_AND_FREE_SERVICES",
        "DISCOUNTS_FOR_FOOD",
        "DISCOUNTS_FOR_DELICACY",
        "SPECIAL_OFFERS_FOR_VETERINARIES",
        "EXIT_DISCOUNTS_AND_FREE_SERVICES",
        "ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS",
        "ABOUT_SERVICES_UNITING_BLIND_PEOPLE",
        "ABOUT_REGIONAL_CLUBS",
        "ABOUT_SPECIAL_VIEW_FOUNDATION",
        "EXIT_SERVICES_FOR_BLIND",
        "INSTRUCTIONS_FOR_LAUNCHING_PODCAST",
    ]

    TRIGGERS_COMMANDS_ANSWERS = [
        (
            getattr(Commands, command_name),
            getattr(Triggers, command_name),
            getattr(GetFunc, command_name),
            getattr(Answers, command_name),
        )
        for command_name in COMMAND_NAMES
    ]
