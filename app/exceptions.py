class AliceException(Exception):
    pass


class QuizException(AliceException):
    pass


class QuizFileNotFoundAliceException(QuizException):
    pass


class QuizFileWrongFormatAliceException(QuizException):
    pass


class QuizFileWrongAnswerAliceException(QuizException):
    pass


class QuizIsFinishedAliceException(QuizException):
    pass


class QuizNoActiveQuestionAliceException(QuizException):
    pass
