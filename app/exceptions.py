class AliceException(Exception):
    pass


class QuizFileNotFoundAliceException(AliceException):
    pass


class QuizFileWrongFormatAliceException(AliceException):
    pass


class QuizFileWrongAnswerAliceException(AliceException):
    pass


class QuizIsFinishedAliceException(AliceException):
    pass


class QuizNoActiveQuestionAliceException(AliceException):
    pass
