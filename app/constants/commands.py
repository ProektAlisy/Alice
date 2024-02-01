class Commands:
    """Класс для хранения команд пользователя.

    Будут заменены на интенты в будущем.
    """

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    about_training_center = (
        "прослушать информацию об учебно-кинологическим "
        "центре собаки-помощники"
    )
    about_staff_1 = "прослушать информацию о персонале центра"
    about_staff_2 = "прослушать информацию о персонале центра продолжение"
    about_staff_3 = "прослушать информацию о персонале центра продолжение 2"
    about_facility = "прослушать описание помещения центра"
    about_training_course = "прослушать информацию о курсе обучения"
    take_manual_training = "пройти обучение по методичке"
    take_quiz = "пройти викторину"
    listen_quiz_results = "узнать результаты викторины"
    listen_to_legislation = "прослушать выдержки из законодательства"
    about_legislation_accessibility = (
        "прослушать информацию о основаниях для доступа к "
        "объектам инфраструктуры"
    )
    about_guide_dog_transportation = "прослушать информацию о провозе собак"
    self_defense_phrase = "прослушать фразу для самозащиты"

    about_discounts_and_free_services = (
        "узнать о скидках/льготах и бесплатных услугах"
    )
    discounts_for_food = "узнать о скидках для питания"
    discounts_for_delicacy = "узнать о скидках на лакомства"
    special_offers_for_veterinaries = (
        "узнать о компенсации расходов на ветеринарию"
    )
    exit_discounts_and_free_services = "выход из скидок и бесплатных услуг"

    about_support_services_for_blind_passengers = (
        "узнать о службах поддержки незрячих пассажиров на транспорте"
    )

    about_services_uniting_blind_people = (
        "узнать о службах объединяющие незрячих"
    )
    about_regional_clubs = "послушать о региональных клубах"
    about_special_view_foundation = "узнать о фонде особый взгляд"
    exit_services_for_blind = "выход из служб поддержки незрячих"

    instructions_for_launching_podcast = (
        "узнать инструкцию запуска подкаста " "министерства наших собачьих дел"
    )
    start = "начинай"
    help_main = "помощь"
    help_phrase = "хочу узнать фразы"
    possibilities = "возможности"


class ServiceCommands:
    """Класс для хранения сервисных команд пользователя."""

    def __setattr__(self, key, value):
        raise AttributeError("Команды изменять нельзя!")

    AGREE = "да"
    DISAGREE = "нет"
    EXIT = "выход"
    NEXT = "дальше"
    REPEAT = "повтори"
