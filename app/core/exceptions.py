class Error(Exception):
    pass


class APIError(Exception):
    def __str__(self):
        return (
            "Что-то случилось с API яндекса или с интернетом."
            "Попробуйте позже."
        )


class StateDumpError(Exception):
    pass


class StateLoadError(Exception):
    pass
