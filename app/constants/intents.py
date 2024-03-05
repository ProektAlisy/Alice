from app.constants.states import HELP_STATES, STATES


class Intents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    def __getattr__(self, name):
        """Выдает атрибуты"""
        if name.lower() in STATES + HELP_STATES:
            return name.upper()
        raise AttributeError(f"Параметр '{name}' не разрешен!")

    ALL_INTENTS = [intent.upper() for intent in STATES + HELP_STATES]
    HELP_INTENTS = [intent.upper() for intent in HELP_STATES]

    @staticmethod
    def get_available(intents: dict[str] | None) -> set[str]:
        """Возвращает список разрешенных интентов.
        Args:
            intents: Список интентов (получен от диалогов)
        Returns:
            Подмножество из intents, которые объявлены в классе.
        """
        return set(STATES + HELP_STATES) & {
            intent.lower() for intent in intents.keys()
        }


INTENTS = Intents()


class ServiceIntents:
    """Класс для хранения сервисных интентов пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = "YANDEX.CONFIRM"
    DISAGREE = "YANDEX.REJECT"
    REPEAT = "YANDEX.REPEAT"
    NEXT = "NEXT"
