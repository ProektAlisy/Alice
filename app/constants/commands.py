from dataclasses import dataclass


@dataclass
class Commands:
    """Класс для хранения команд пользователя."""

    ABOUT_TRAINING_CENTER: str = (
        "Прослушать информацию об учебно-"
        "кинологическом центре собаки-помощники"
    )
    ABOUT_FACILITY: str = "Прослушать описание помещения центра"
    ABOUT_STAFF_1: str = "Прослушать информацию о персонале центра"
    ABOUT_STAFF_2: str = "Прослушать информацию о персонале центра продолжение"
    ABOUT_STAFF_3: str = (
        "Прослушать информацию о персонале центра продолжение 2"
    )
    ABOUT_TRAINING_COURSE: str = "Прослушать информацию о курсе обучения"
    TAKE_MANUAL_TRAINING: str = "пройти обучение по методичке"
    TAKE_QUIZ: str = "Пройти викторину"
    LISTEN_TO_LEGISLATION: str = "Прослушать выдержки из законодательства"
    ABOUT_LEGISLATION_ACCESSIBILITY: str = (
        "Прослушать информацию о основаниях для доступа к "
        "объектам инфраструктуры"
    )
    CHOICE_BY_LAND_RAIL_AIR_WATER: str = (
        "Выбор информации о провозе собаки в различных видах транспорта"
    )
    ABOUT_TRANSPORTATION_BY_LAND_TRANSPORT: str = (
        "Узнать о провозе собак-проводников в наземном транспорте"
    )
    ABOUT_TRANSPORTATION_BY_RAIL: str = (
        "Узнать о провозе собак-проводников в железнодорожном транспорте"
    )
    ABOUT_AIR_TRANSPORTATION: str = (
        "Узнать о провозе собак-проводников в воздушном транспорте"
    )
    ABOUT_TRANSPORTATION_BY_WATER: str = (
        "Узнать о провозе собак-проводников в водном транспорте"
    )
    SELF_DEFENSE_PHRASE: str = "Прослушать фразу для самозащиты"
    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS: str = (
        "Узнать о службах поддержки незрячих пассажиров на транспорте"
    )
    ABOUT_DISCOUNTS_AND_FREE_SERVICES: str = (
        "Узнать о скидках/льготах и бесплатных услугах"
    )
    DISCOUNTS_FOR_FOOD: str = "Узнать о скидках для питания"
    DISCOUNTS_FOR_DELICACY: str = "Узнать о скидках на лакомства"
    SPECIAL_OFFERS_FOR_VETERINARIES: str = (
        "Узнать о компенсации расходов на ветеринарию"
    )
    ABOUT_SERVICES_UNITING_BLIND_PEOPLE: str = (
        "Узнать о службах объединяющие незрячих"
    )
    ABOUT_REGIONAL_CLUBS: str = "Прослушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION: str = "Узнать о фонде особый взгляд"
    ABOUT_PODCAST: str = "Узнать о подкасте"
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST: str = (
        "Узнать инструкцию запуска подкаста министерства наших собачьих дел"
    )


@dataclass
class HelpCommands:
    HELP_MAIN: str = "помощь"
    HELP_PHRASE: str = "хочу узнать фразы"
    POSSIBILITIES: str = "возможности"
    USEFUL_INFORMATION: str = "полезная информация"


class ServiceCommands:
    """Класс для хранения сервисных команд пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = (
        "да",
        "начинай",
        "давай",
    )
    DISAGREE = (
        "нет",
        "не надо",
    )
    EXIT = "выход из навыка"
    NEXT = "дальше"
    REPEAT = "повтори"


ALICE_COMMANDS = set()
with open(
    "app/constants/alice_commands.txt",
    "r",
    encoding="utf-8",
) as file:
    ALICE_COMMANDS = {line.strip() for line in file}
