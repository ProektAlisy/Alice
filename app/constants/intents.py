class Intents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    TAKE_QUIZ = "take_quiz"  # 'Запусти викторину', 'включи викторину'
    AGREE = "agree"  # 'Давай', 'Начинай', 'Хочу', 'дальше', 'попробуем', 'согласен'
    REPEAT = "YANDEX.REPEAT"
    START_AGAIN = "start_again"  # 'Начать заново' 'Запустить с начала'
    NO_ANSWER = "no_answer"  # TODO
