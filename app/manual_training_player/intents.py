class ManualTrainingIntents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    REPEAT = "YANDEX.REPEAT"
    CONFIRM = "YANDEX.CONFIRM"
    REJECT = "YANDEX.REJECT"

    TAKE_MANUAL_TRAINING = "take_manual_training"  # Начать прослушивание методички
    RESUME_MANUAL_TRAINING = "resume_manual_training"  # Продолжить прослушивание методички
    PAUSE_MANUAL_TRAINING = "pause_manual_training"  # Поставить прослушивание методички на паузу
    NEXT_MANUAL_TRAINING_CHAPTER = "next_manual_training_chapter"  # Перейти к следующей главе методички
    SHOW_MANUAL_TRAINING_CONTENTS = "show_manual_training_contents"  # Показать оглавление методички
    CHOOSE_MANUAL_TRAINING_CHAPTER = "choose_manual_training_chapter"  # Выбрать конкретную главу методички
    TERMINATE_MANUAL_TRAINING = "terminate_manual_training"  # Остановить обучение по методичке
