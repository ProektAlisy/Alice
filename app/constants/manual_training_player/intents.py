class ManualTrainingIntents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    REPEAT = "YANDEX.REPEAT"
    CONFIRM = "YANDEX.CONFIRM"
    REJECT = "YANDEX.REJECT"

    START_MANUAL_TRAINING = "start_manual_training"
    RESUME_MANUAL_TRAINING = "resume_manual_training"
    PAUSE_MANUAL_TRAINING = "pause_manual_training"
    NEXT_MANUAL_TRAINING_CHAPTER = "next_manual_training_chapter"
    SHOW_MANUAL_TRAINING_CONTENTS = "show_manual_training_contents"
    CHOOSE_MANUAL_TRAINING_CHAPTER = "choose_manual_training_chapter"
    TERMINATE_MANUAL_TRAINING = "terminate_manual_training"
    GET_MANUAL_TRAINING_CHAPTER_INFO = "get_manual_training_chapter_info"
