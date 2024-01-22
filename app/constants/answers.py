class Answers:
    def __setattr__(self, key, value):
        raise AttributeError("Messages is immutable")

    DONT_UNDERSTAND = "Я не понимаю, что вы хотите сказать"
    SMALL_GREETINGS = """
    Вы приехали к нам на обучение, чтобы получить 
    долгожданную собаку-поводыря. Добро пожаловать! Сейчас запущен навык 
    Собаки-помощники.\n
        """.replace(
        "\n", " "
    )

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
    ABOUT_TRAINING_CENTER = "Здесь будет информация о центре"
    ABOUT_STAFF = "Здесь будет информация о персонале центра"
    ABOUT_ACCOMMODATION = "Здесь будет информация о проживании в центре"
    ABOUT_FACILITY = "Здесь будет информация о помещении центра"
    TAKE_TRAINING = (
        "Здесь будет информация о прохождении обучения по методичке"
    )
    TAKE_QUIZ = "Здесь будет информация о прохождении викторины"

    LISTEN_TO_LEGISLATION = (
        "Здесь будет информация о выдержках из законодательства"
    )
    ABOUT_ACCESSIBILITY = "Здесь будет информация о основаниях для доступа к объектам инфраструктуры"
    ABOUT_GUIDE_DOG_TRANSPORTATION = "Здесь будет информация о провозе собак"
    SELF_DEFENSE_PHRASE = "Здесь будет информация о фразы для самозащиты"

    ABOUT_DISCOUNTS_AND_FREE_SERVICES = (
        "Здесь будет информация о скидках или льготах"
    )
    DISCOUNTS_FOR_FOOD = "Здесь будет информация о скидках для питания"
    DISCOUNTS_FOR_DELICACY = "Здесь будет информация о скидках на лакомства"
    SPECIAL_OFFERS_FOR_VETERINARIES = (
        "Здесь будет информация о компенсации расходов на ветеринарию"
    )

    ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS = (
        "Здесь будет информация о службах поддержки"
    )
    ABOUT_SERVICES_UNITING_BLIND_PEOPLE = (
        "Здесь будет информация о службах поддержки незрячих"
    )
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "Здесь будет информация о запуске подкаста"
    )

    ABOUT_REGIONAL_CLUBS = "Здесь будет информация о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = (
        "Здесь будет информация о фонде Особый взгляд"
    )

    ALL_COMPLETED = "Все задания выполнены. Спасибо за обучение"

    EXIT_FROM_SKILL = "Вы вышли из навыка Собаки-помощники"
    EXIT_FROM_HELP = "Вы вышли из помощи"
    EXIT_FROM_LEGISLATION = "Вы вышли из законодательства"
    EXIT_DISCOUNTS_AND_FREE_SERVICES = "Вы вышли из скидок"
    EXIT_SERVICES_FOR_BLIND = "Вы вышли из служб поддержки незрячих"

    HELP = "Помощь"
    HELP_NAVIGATION = "Помощь в навигации по центру"
    HELP_PHRASE = "Помощь по фразам взаимодействия с навыком"
    HELP_MAIN = (
        "Здесь вы можете узнать фразы взаимодействия или получить "
        "помощь с навигацией по навыку!"
    )