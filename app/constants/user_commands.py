from app.constants.answers import Answers


class Commands:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    # основные истории
    ABOUT_TRAINING_CENTER = "прослушать информацию об учебно-кинологическим центре собаки-помощники"
    ABOUT_ACCOMMODATION = "прослушать информацию о проживании в центре"
    ABOUT_STAFF = "прослушать информацию о персонале центра"
    ABOUT_FACILITY = "прослушать описание помещения центра"
    TAKE_TRAINING = "пройти обучение"
    TAKE_QUIZ = "пройти викторину"
    LISTEN_TO_LEGISLATION = "прослушать выдержки из законодательства"
    ABOUT_DISCOUNTS_AND_FREE_SERVICES = (
        "узнать о скидках/льготах и бесплатных услугах"
    )
    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = (
        "узнать о службах объединяющие незрячих"
    )
    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "узнать о службах поддержки незрячих пассажиров на транспорте"
    )
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "узнать инструкцию запуска подкаста "
        "'министерства наших собачьих дел'"
    )
    # вложенные истории (узнать о службах объединяющие незрячих,
    # ABOUT_SERVICES_UNITING_BLIND_PEOPLE)
    ABOUT_REGIONAL_CLUBS = "послушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "узнать о фонде особый взгляд"
    # вложенные истории (Послушать выдержки из законодательства,
    # LISTEN_TO_LEGISLATION)
    ABOUT_ACCESSIBILITY = (
        "узнать об основаниях для беспрепятственного "
        "доступа к объектам социальной инфраструктуры"
    )
    ABOUT_GUIDE_DOG_TRANSPORTATION = (
        "узнать о провозе собак-проводников в транспорте"
    )
    SELF_DEFENSE_PHRASE = (
        "узнать фразу, которая поможет защитить себя, "
        "если вас не пускают куда-то"
    )
    # вложенные истории (узнать о скидках/льготах и бесплатных услугах,
    # ABOUT_DISCOUNTS_AND_FREE_SERVICES)
    ABOUT_DISCOUNTS_ON_FOOD = "узнать про скидки на корм"
    ABOUT_DISCOUNTS_ON_TREATS = "узнать про скидки на лакомства"
    COMPENSATION_INFORMATION = (
        "узнать про компенсацию расходов на содержание "
        "и ветеринарное обслуживание"
    )
    # все, что относится к помощи.
    HELP = "помощь"
    HELP_PHRASE = "помощь по фразам"
    HELP_NAVIGATION = "помощь по навигации"
    HELP_EXIT = "выход из помощи"
    EXIT = "выход"
    NEXT = "следующее"


class Default:
    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    TRIGGERS_COMMANDS_ANSWERS = (
        (Commands.ABOUT_TRAINING_CENTER, "trigger_training_center", "get_training_center", Answers.INFO_ABOUT_CENTER,),
        (Commands.ABOUT_STAFF, "trigger_staff", "get_staff", Answers.INFO_ABOUT_STAFF),
        (Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE, "trigger_services_for_blind", "get_services_for_blind", Answers.SERVICES_FOR_BLIND),
        # "trigger_help",
        # "trigger_help_phrase",
        # "trigger_help_navigation",
        # "trigger_help_exit",
        # "trigger_exit",
    )
    ORDER_COMMANDS = [
        Commands.ABOUT_TRAINING_CENTER,
        Commands.ABOUT_STAFF,
        Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
        # Commands.ABOUT_ACCOMMODATION,
        # Commands.ABOUT_FACILITY,
        # Commands.TAKE_TRAINING,
        # Commands.TAKE_QUIZ,
        # Commands.LISTEN_TO_LEGISLATION,
        # Commands.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
        # Commands.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
        # Commands.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
    ]
