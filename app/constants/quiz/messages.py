from typing import Final


class QuizExceptionMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    QUIZ_FILE_WRONG_FORMAT: Final = "Ошибка формата в файле вопросов викторины"
    QUIZ_FILE_WRONG_ANSWER: Final = """
    Неизвестный ответ <{answer}> в файле вопросов викторины для вопроса
    <{question}>
    """
    QUIZ_IS_FINISHED: Final = (
        "Все вопросы викторины заданы. Викторина завершена!"
    )
    NO_ACTIVE_QUESTION_ERROR: Final = "Нет текущего вопроса для проверки!"


class QuizMessages:
    def __setattr__(self, key, value):
        raise AttributeError("Messages are immutable")

    CHOICE_FORMAT: Final = "{key}) sil <[300]> {value}. sil <[300]>"
    QUESTION_AND_CHOICES_FORMAT: Final = "{question}\n{choices}\n"
    FULL_QUESTION_FORMAT: Final = """
    Вопрос номер {current_question_number}.
    {question_and_choices}
    Ваш вариант ответа:
    """
    RULES: Final = (
        """Вы оказались в разделе, где можете проверить насколько
        усвоен пройденный теоретический материал.
        Я задам Вам {total_questions_count} вопросов, и после каждого вопроса
        предложу три варианта ответа. sil <[300]>
        Вам надо выбрать единственный правильный ответ.
        Для ответа просто назовите букву с правильным ответом: А, Бэ или Вэ.
        Если чувствуете, что Вам пока не хватает знаний, скажите:
        'Завершить викторину'. sil <[300]>
        Если нужно повторить вопрос и варианты ответов, скажите: 'Повтори'.
        sil <[300]> Приступ+аем?
        """.replace(
            "\n",
            " ",
        )
    )

    RULES_CHOICES: Final = (
        """Если хотите начать викторину, скажите sil <[300]>
        'Приступаем', иначе скажите sil <[300]> 'Заверши викторину'.
        sil <[300]> Что вы решили, приступаем?
        """.replace(
            "\n",
            " ",
        )
    )

    ALREADY_IN_PROGRESS: Final = (
        """Вы вернулись. Как здорово! Напоминаю правила: Я задаю вопрос и
        предлагаю Вам на выбор три варианта ответа. Для ответа просто назовите
        букву с правильным ответом: А, Б или В. Правильный ответ может быть
        только один. У Вас есть незаконченная викторина. Сейчас вы остановились
        на вопросе номер {current_question_number}. Продолжим ее?
        Чтобы начать викторину заново скажите 'Начать заново'.
        """.replace(
            "\n",
            " ",
        )
    )
    RESUME_REPEAT: Final = (
        """Сейчас вы остановились на вопросе номер {current_question_number}.
        Чтобы продолжить викторину скажите 'Продолжим'.
        Чтобы начать викторину заново скажите 'Начать заново'.
        Чтобы завершить викторину скажите 'Завершить викторину'.
        """.replace(
            "\n",
            " ",
        )
    )

    ALREADY_FINISHED: Final = "Викторина уже пройдена."
    RESET_PROGRESS: Final = """
    Чтобы начать викторину заново скажите 'Начать заново'.
    Это удалит весь предыдущий прогресс. Начать заново?
    """
    CHOICE_HELP: Final = """
    Чтобы ответить на вопрос назовите букву с правильным вариантом ответа
    А, sil <[200]> Б sil <[200]> или В.
    """
    CORRECT_ANSWER_FORMAT: Final = (
        "Правильный ответ '{choice}') sil <[200]> {answer}. sil <[500]>"
    )
    RESULT_EXCELLENT: Final = """
    Превосходный результат!
    Вы ответили на все {total} вопросов без ошибок.
    """
    RESULT_GOOD_1: Final = "Неплохой результат, всего одна ошибка."
    RESULT_GOOD_2: Final = "Неплохой результат, всего две ошибки."
    RESULT_NOT_BAD_3_4: Final = """
    Вы допустили {mistakes} ошибки.
    Не плохо, но думаю, стоит еще поучиться.
    """
    RESULT_BAD: Final = """Вы допустили {mistakes} ошибок, это довольно много.
        Стоит еще поучиться.
        """
    RESULT_VERY_BAD: Final = (
        "Вы допустили {mistakes} ошибок, это очень много. Стоит еще поучиться."
    )
    # форматы ответов при досрочном выходе
    PARTIAL_RESULT_0: Final = """
    Хорошо, завершаю викторину, но хочу сказать, что Вы отлично справились,
    не допустив ни одной ошибки.
    """
    PARTIAL_RESULT_1: Final = """
    Вы допустили всего одну ошибку. Не плохой результат.
    Завершаю викторину и жду Вашего возвращения.
    """
    PARTIAL_RESULT_NOT_BAD: Final = """
    Вы допустили {mistakes} ошибки. Не плохо, но думаю, стоит еще поучиться.
    Завершаю викторину и жду Вашего возвращения.
    """
    PARTIAL_RESULT_BAD: Final = """
    Вы допустили {mistakes} ошибок, это довольно много. Стоит еще поучиться.
    Завершаю викторину, но очень жду Вашего возвращения|
    """
    CORRECT_VARIANTS: Final = [
        "Поздравляю, это правильный ответ!",
        "Верно.",
        "Вы молодец.",
        "Потрясающе.",
        "Великолепно.",
    ]
    INCORRECT_VARIANTS: Final = [
        "К сожалению, нет.",
        "Ответ неверный.",
        "Не совсем так.",
    ]
    CHEER_UP_VARIANTS: Final = [
        """Не страшно, Вы здесь чтобы учиться.
        Попробуйте угадать ответ, а я Вам расскажу какой ответ правильный.
        """,
        """В теории мы это точно проходили, попробуйте вспомнить.
        Ничего страшного, если ошибетесь.
        """,
        "Давайте проверим вашу интуицию! Если не угадаете, я Вас поправлю.",
    ]
    NO_RESULTS: Final = """
    Завершаю викторину и жду Вашего возвращения sil <[200]>.
    """
    NO_QUIZ: Final = "Викторина временно недоступна!"
    UNKNOWN_COMMAND: Final = "Неизвестная команда!"
    AFTER_QUIZ: Final = "."
