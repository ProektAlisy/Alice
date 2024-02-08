class Commands:
    """Класс для хранения команд пользователя.

    Будут заменены на интенты в будущем.
    """

    def setattr(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    ABOUT_TRAINING_CENTER = (
        "Прослушать информацию об учебно-кинологическом "
        "центре собаки-помощники"
    )
    ABOUT_FACILITY = "Прослушать описание помещения центра"
    ABOUT_STAFF_1 = "Прослушать информацию о персонале центра"
    ABOUT_STAFF_2 = "Прослушать информацию о персонале центра продолжение"
    ABOUT_STAFF_3 = "Прослушать информацию о персонале центра продолжение 2"
    ABOUT_TRAINING_COURSE = "Прослушать информацию о курсе обучения"
    TAKE_MANUAL_TRAINING = "Пройти обучение по методичке"
    TAKE_QUIZ = "Пройти викторину"
    LISTEN_TO_LEGISLATION = "Прослушать выдержки из законодательства"
    ABOUT_LEGISLATION_ACCESSIBILITY = (
        "Прослушать информацию о основаниях для доступа к "
        "объектам инфраструктуры"
    )
    ABOUT_GUIDE_DOG_TRANSPORTATION = "Прослушать информацию о провозе собак"
    ABOUT_TRANSPORTATION_BY_LAND_TRANSPORT = (
        "Узнать о провозе собак-проводников в наземном транспорте"
    )
    ABOUT_TRANSPORTATION_BY_RAIL = (
        "Узнать о провозе собак-проводников в железнодорожном транспорте"
    )
    ABOUT_AIR_TRANSPORTATION = (
        "Узнать о провозе собак-проводников в воздушном транспорте"
    )
    ABOUT_TRANSPORTATION_BY_WATER = (
        "Узнать о провозе собак-проводников в водном транспорте"
    )
    SELF_DEFENSE_PHRASE = "Прослушать фразу для самозащиты"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = (
        "Узнать о скидках/льготах и бесплатных услугах"
    )
    DISCOUNTS_FOR_FOOD = "Узнать о скидках для питания"
    DISCOUNTS_FOR_DELICACY = "Узнать о скидках на лакомства"
    SPECIAL_OFFERS_FOR_VETERINARIES = (
        "Узнать о компенсации расходов на ветеринарию"
    )
    EXIT_DISCOUNTS_AND_FREE_SERVICES = "Выход из скидок и бесплатных услуг"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "Узнать о службах поддержки незрячих пассажиров на транспорте"
    )

    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = (
        "Узнать о службах объединяющие незрячих"
    )
    ABOUT_REGIONAL_CLUBS = "Прослушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "Узнать о фонде особый взгляд"
    EXIT_SERVICES_FOR_BLIND = "Выход из служб поддержки незрячих"

    ABOUT_PODCAST = "Узнать о подкасте"
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "Узнать инструкцию запуска подкаста министерства наших собачьих дел"
    )
    HELP_MAIN = "Помощь"
    HELP_PHRASE = "Хочу узнать фразы"
    POSSIBILITIES = "Возможности"
    USEFUL_INFORMATION = "Полезная информация"


class ServiceCommands:
    """Класс для хранения сервисных команд пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = "да"
    DISAGREE = "нет"
    EXIT = "выход"
    NEXT = "дальше"
    REPEAT = "повтори"
