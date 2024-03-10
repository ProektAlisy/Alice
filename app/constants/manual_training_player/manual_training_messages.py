from typing import Final

from app import settings


class ManualPlayerMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    TRAINING_COMPLETED: Final = "Обучение уже завершено."
    UNKNOWN_COMMAND: Final = "Неизвестная команда."
    NO_CHAPTER: Final = (
        "Указанная глава не существует. sil <[400]>"
        "Пожалуйста, выберите другую главу."
    )
    CHAPTER_NAME: Final = "Название главы {chapter_number}: {chapter_name}."
    CHAPTER_NUMBER_NOT_FOUND: Final = "Глава с указанным номером не найдена."
    NO_CHAPTER_NUMBER: Final = "Не указан номер главы."
    INVALID_CHAPTER_NUMBER: Final = "Неверный формат номера главы."
    PLAYBACK_NOT_STARTED: Final = "Проигрывание еще не началось."
    PLAYBACK_IS_ACTIVE: Final = "Проигрывание уже идёт."
    MANUAL_END: Final = "Вы достигли конца книги."
    NO_CURRENT_CHAPTER: Final = "Нет текущей главы для продолжения."
    PLAYBACK_STOP: Final = "Остановила."
    ALREADY_FINISHED: Final = "Обучение по методичке уже завершено."
    PLAYBACK_START: Final = (
        "Начинаю проигрывание главы номер "
        "{chapter_number} - {chapter_name}."
    )
    CHAPTER_AUDIO_URL: Final = f"{settings.BASE_AUDIO_URL}""{chapter_name}.mp3"
    CONTENT: Final = "Оглавление: sil <[300]>"
    CONTENT_CHAPTER: Final = "Глава {chapter_num} - {title}. sil <[300]>"
