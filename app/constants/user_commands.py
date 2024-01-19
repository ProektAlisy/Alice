from app.constants.answers import Answers


class Commands:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    # основные команды для историй
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
    EXIT_FROM_LEGISLATION = "выйти из законодательства"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = (
        "узнать о скидках/льготах и бесплатных услугах"
    )
    DISCOUNTS_FOR_FOOD = "узнать о скидках для питания"
    DISCOUNTS_FOR_DELICACY = "узнать о скидках на лакомства"
    SPECIAL_OFFERS_FOR_VETERINARIES = (
        "узнать о компенсации расходов на ветеринарию"
    )

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "узнать о службах поддержки незрячих пассажиров на транспорте"
    )
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "узнать инструкцию запуска подкаста "
        "'министерства наших собачьих дел'"
    )
    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = (
        "узнать о службах объединяющие незрячих"
    )
    ABOUT_REGIONAL_CLUBS = "послушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "узнать о фонде особый взгляд"

    HELP = "помощь"
    HELP_PHRASE = "помощь по фразам"
    HELP_NAVIGATION = "помощь по навигации"
    HELP_EXIT = "выход из помощи"
    EXIT = "выход"
    NEXT = "следующее"


class Triggers:
    def __setattr__(self, key, value):
        raise AttributeError("Триггеры изменять нельзя!")

    TRAINING_CENTER = "trigger_training_center"
    STAFF = "trigger_staff"
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
    DISCOUNT_EXIT = "trigger_discounts_free_services_exit"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "trigger_support_services_blind"
    )
    SERVICES_FOR_BLIND = "trigger_services_for_blind"
    ABOUT_REGIONAL_CLUBS = "trigger_regional_clubs"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "trigger_special_view_foundation"
    SERVICES_FOR_BLIND_EXIT = "trigger_services_for_blind_exit"

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

    TRAINING_CENTER = "get_training_center"
    STAFF = "get_staff"
    SERVICES_FOR_BLIND = "get_services_for_blind"
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

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = "get_support_services_blind"
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "get_launch_podcast"
    ABOUT_REGIONAL_CLUBS = "get_regional_clubs"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "get_special_view_foundation"

    HELP = "get_help"
    HELP_PHRASE = "get_help_phrase"
    HELP_NAVIGATION = "get_help_navigation"
    HELP_EXIT = "get_help_exit"
    EXIT = "get_exit"
    NEXT = "get_next"


class TrigComAns:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    TRIGGERS_COMMANDS_ANSWERS = (
        (
            Commands.ABOUT_TRAINING_CENTER,
            Triggers.TRAINING_CENTER,
            GetFunc.TRAINING_CENTER,
            Answers.INFO_ABOUT_CENTER,
        ),
        (
            Commands.ABOUT_STAFF,
            Triggers.STAFF,
            GetFunc.STAFF,
            Answers.INFO_ABOUT_STAFF,
        ),
        (
            Commands.ABOUT_ACCOMMODATION,
            Triggers.ABOUT_ACCOMMODATION,
            GetFunc.ABOUT_ACCOMMODATION,
            Answers.ABOUT_ACCOMMODATION,
        ),
        (
            Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
            Triggers.SERVICES_FOR_BLIND,
            GetFunc.SERVICES_FOR_BLIND,
            Answers.SERVICES_FOR_BLIND,
        ),
        (
            Commands.ABOUT_FACILITY,
            Triggers.ABOUT_FACILITY,
            GetFunc.ABOUT_FACILITY,
            Answers.ABOUT_FACILITY,
        ),
        (
            Commands.TAKE_TRAINING,
            Triggers.TAKE_TRAINING,
            GetFunc.TAKE_TRAINING,
            Answers.TAKE_TRAINING,
        ),
        (
            Commands.TAKE_QUIZ,
            Triggers.TAKE_QUIZ,
            GetFunc.TAKE_QUIZ,
            Answers.TAKE_QUIZ,
        ),
        (
            Commands.LISTEN_TO_LEGISLATION,
            Triggers.LISTEN_TO_LEGISLATION,
            GetFunc.LISTEN_TO_LEGISLATION,
            Answers.LISTEN_TO_LEGISLATION,
        ),
        (
            Commands.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
            Triggers.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
            GetFunc.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
            Answers.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
        ),
        (
            Commands.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
            Triggers.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
            GetFunc.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
            Answers.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
        ),
        (
            Commands.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
            Triggers.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
            GetFunc.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
            Answers.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
        ),
        (
            Commands.ABOUT_REGIONAL_CLUBS,
            Triggers.ABOUT_REGIONAL_CLUBS,
            GetFunc.ABOUT_REGIONAL_CLUBS,
            Answers.ABOUT_REGIONAL_CLUBS,
        ),
        (
            Commands.ABOUT_SPECIAL_VIEW_FOUNDATION,
            Triggers.ABOUT_SPECIAL_VIEW_FOUNDATION,
            GetFunc.ABOUT_SPECIAL_VIEW_FOUNDATION,
            Answers.ABOUT_SPECIAL_VIEW_FOUNDATION,
        ),
        (
            Commands.ABOUT_ACCESSIBILITY,
            Triggers.ABOUT_ACCESSIBILITY,
            GetFunc.ABOUT_ACCESSIBILITY,
            Answers.ABOUT_ACCESSIBILITY,
        ),
        (
            Commands.ABOUT_GUIDE_DOG_TRANSPORTATION,
            Triggers.ABOUT_GUIDE_DOG_TRANSPORTATION,
            GetFunc.ABOUT_GUIDE_DOG_TRANSPORTATION,
            Answers.ABOUT_GUIDE_DOG_TRANSPORTATION,
        ),
        (
            Commands.SELF_DEFENSE_PHRASE,
            Triggers.SELF_DEFENSE_PHRASE,
            GetFunc.SELF_DEFENSE_PHRASE,
            Answers.SELF_DEFENSE_PHRASE,
        ),
        (
            Commands.EXIT_FROM_LEGISLATION,
            Triggers.EXIT_FROM_LEGISLATION,
            GetFunc.EXIT_FROM_LEGISLATION,
            Answers.EXIT_FROM_LEGISLATION,
        ),
    )
