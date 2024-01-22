class Answers:
    def __setattr__(self, key, value):
        raise AttributeError("Messages is immutable")

    DONT_UNDERSTAND = "Я не понимаю, что вы хотите сказать"
    SMALL_GREETINGS = """
    Вы приехали к нам на обучение, чтобы получить 
    долгожданную собаку-поводыря. Добро пожаловать! Сейчас запущен навык 
    "Собаки-помощники".replace("\n", " ")
    """
    FULL_GREETINGS = """
     Здесь я расскажу Вам информацию о нашем центре, о том, как проходит
     проживание, о его персонале, опишу помещение центра. Помогу с обучением,
     после которого вы сможете проверить свои знания в викторине.
     А также расскажу, о законодательной базе, о льготах и скидках для
     владельцев собак-поводырей, о службах поддержки незрячих пассажиров в
     транспорте, об объединениях незрячих людей, и о том как можно 
     запустить подкаст. Если необходимо повторить скажите "повтори". Назовите,
     что Вас заинтересовало или скажите "Начинай" и я начну по порядку с 
     описания центра.
    """.replace(
        "\n    ", " "
    )
    SERVICES_FOR_BLIND = "Здесь будет информация о службах поддержки незрячих"
    INFO_ABOUT_STAFF = "Здесь будет информация о персонале центра"
    INFO_ABOUT_CENTER = "Здесь будет информация о центре"
    ALL_COMPLETED = "Все задания выполнены. Спасибо за обучение"
    EXIT_FROM_SKILL = "Вы вышли из навыка Собаки-помощники"
    EXIT_FROM_HELP = "Вы вышли из помощи"
    HELP_NAVIGATION = "Помощь в навигации по центру"
    HELP_PHRASE = "Помощь по фразам взаимодействия с навыком"
    HELP_MAIN = (
        "Здесь вы можете узнать фразы взаимодействия или получить "
        "помощь с навигацией по навыку!"
    )

    ANSWERS_OUTPUT = {INFO_ABOUT_CENTER: "get_help"}
