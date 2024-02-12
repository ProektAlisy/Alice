from typing import Optional


class Intents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    ABOUT_TRAINING_CENTER = "ABOUT_TRAINING_CENTER"
    ABOUT_FACILITY = "ABOUT_FACILITY"
    ABOUT_STAFF_1 = "ABOUT_STAFF_1"
    ABOUT_STAFF_2 = "ABOUT_STAFF_2"
    ABOUT_STAFF_3 = "ABOUT_STAFF_CAT"
    ABOUT_TRAINING_COURSE = "ABOUT_TRAINING_COURSE"
    TAKE_MANUAL_TRAINING = "TAKE_MANUAL_TRAINING"
    TAKE_QUIZ = "TAKE_QUIZ_mock"
    LISTEN_TO_LEGISLATION = "LISTEN_TO_LEGISLATION"
    ABOUT_LEGISLATION_ACCESSIBILITY = "ABOUT_LEGISLATION_ACCESSIBILITY"
    ABOUT_GUIDE_DOG_TRANSPORTATION = "ABOUT_GUIDE_DOG_TRANSPORTATION"
    ABOUT_TRANSPORTATION_BY_LAND_TRANSPORT = (
        "ABOUT_TRANSPORTATION_BY_LAND_TRANSPORT"
    )
    ABOUT_TRANSPORTATION_BY_RAIL = "ABOUT_TRANSPORTATION_BY_RAIL"
    ABOUT_AIR_TRANSPORTATION = "ABOUT_AIR_TRANSPORTATION"
    ABOUT_TRANSPORTATION_BY_WATER = "ABOUT_TRANSPORTATION_BY_WATER"
    SELF_DEFENSE_PHRASE = "SELF_DEFENSE_PHRASE"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = "ABOUT_DISCOUNTS_AND_FREE_SERVICES"
    DISCOUNTS_FOR_FOOD = "DISCOUNTS_FOR_FOOD"
    DISCOUNTS_FOR_DELICACY = "DISCOUNTS_FOR_DELICACY"
    SPECIAL_OFFERS_FOR_VETERINARIES = "SPECIAL_OFFERS_FOR_VETERINARIES"

    EXIT_DISCOUNTS_AND_FREE_SERVICES = "EXIT_DISCOUNTS_AND_FREE_SERVICES"

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS"
    )

    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = "ABOUT_SERVICES_UNITING_BLIND_PEOPLE"
    ABOUT_REGIONAL_CLUBS = "ABOUT_REGIONAL_CLUBS"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "ABOUT_SPECIAL_VIEW_FOUNDATION"
    EXIT_SERVICES_FOR_BLIND = "EXIT_SERVICES_FOR_BLIND"

    ABOUT_PODCAST = "ABOUT_PODCAST"
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = "INSTRUCTIONS_FOR_LAUNCHING_PODCAST"
    HELP_MAIN = "YANDEX.HELP"
    HELP_PHRASE = "HELP_PHRASE"
    POSSIBILITIES = "POSSIBILITIES"
    USEFUL_INFORMATION = "USEFUL_INFORMATION"

    @classmethod
    def get_available(cls, intents: Optional[list[str]]) -> set[str]:
        """Возвращает список разрешенных интентов.

        Args:
            intents (list[str]): Список интентов (получен от диалогов)

        Returns:
            set[str]: Подмножество из intents, которые объявлены в классе.

        """
        return {
            var for var in cls.__dict__.values() if not callable(var)
        } & set(intents)


class ServiceIntents:
    """Класс для хранения сервисных интентов пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = "YANDEX.CONFIRM"
    DISAGREE = "YANDEX.REJECT"
    # EXIT = "выход"
    # NEXT = "дальше"
    REPEAT = "YANDEX.REPEAT"
