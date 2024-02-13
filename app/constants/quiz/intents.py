class QuizIntents:
    """Класс для используемых команд намерений (intents)."""

    def __setattr__(self, key, value):
        raise AttributeError("Интенты изменять нельзя!")

    TAKE_QUIZ = "take_quiz"  # 'Запусти викторину', 'включи викторину'
    AGREE = "agree"  # 'Давай', 'Начинай', 'Хочу', 'дальше', 'попробуем'
    REPEAT = "YANDEX.REPEAT"
    START_AGAIN = "start_again"  # 'Начать заново' 'Запустить с начала'
    CONTINUE = "continue"  # продолжим, дальше, давай
    NO_ANSWER = "no_answer"  # 'не знаю', 'забыл', 'затрудняюсь ответить'
    TERMINATE_QUIZ = "terminate_quiz"  # 'остановить викторину', 'завершить...'
    CONFIRM = "YANDEX.CONFIRM"
    REJECT = "YANDEX.REJECT"
