from typing import Optional

from app.constants.states import STATES, HELP_STATES


class Intents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    def __getattr__(self, name):
        if name.lower() in STATES + HELP_STATES:
            return name.upper()
        else:
            raise AttributeError(f"Параметр '{name}' не разрешен!")

    @staticmethod
    def get_available(intents: Optional[dict[str]]) -> set[str]:
        """Возвращает список разрешенных интентов.
        Args:
            intents (list[str]): Список интентов (получен от диалогов)
        Returns:
            set[str]: Подмножество из intents, которые объявлены в классе.
        """
        return set(STATES + HELP_STATES) & set(intents)


INTENTS = Intents()


class ServiceIntents:
    """Класс для хранения сервисных интентов пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = "YANDEX.CONFIRM"
    DISAGREE = "YANDEX.REJECT"
    REPEAT = "YANDEX.REPEAT"
