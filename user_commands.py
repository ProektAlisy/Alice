class Commands:
    def __setattr__(self, key, value):
        raise AttributeError("Messages is immutable")

    ABOUT_CUSTOMER_SERVICE = "узнать о службах поддержки"
    INSTRUCTIONS_FOR_LAUNCHING_PODCAST = (
        "узнать инструкцию запуска подкаста "
        "'Министерства наших собачьих дел'"
    )
    ABOUT_DISCOUNTS_AND_SPECIAL_OFFERS = "узнать о скидках и спецпредложениях"
    ABOUT_REGIONAL_CLUBS = "послушать о региональных клубах"
    ABOUT_SPECIAL_VIEW_FOUNDATION = "узнать о фонде особый взгляд"
    INFO_ABOUT_CENTER = "прослушать информацию о центре"
    INFO_ABOUT_CENTER_PERSONAL = "прослушать информацию о персонале"
    HELP = "помощь"
    HELP_PHRASE = "помощь по фразам"
    HELP_NAVIGATION = "помощь по навигации"
    HELP_EXIT = "выход из помощи"
    EXIT = "выход"
    SERVICES_FOR_BLIND = "узнать о службах, объединяющие незрячих"
