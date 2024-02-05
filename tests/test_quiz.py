import pytest

from app.quiz import (
    Quiz,
    QuizFileNotFoundAliceException,
    QuizFileWrongAnswerAliceException,
    QuizFileWrongFormatAliceException,
    QuizIsFinishedAliceException,
    QuizNoActiveQuestionAliceException,
)


def test_load_from_wrong_file_name():
    """Загрузка из отсутствующего файла взводит QuizFileNotFoundAliceException"""
    quiz = Quiz()
    with pytest.raises(QuizFileNotFoundAliceException):
        quiz.load_questions("wrong_file_name.json")


def test_load_from_file_wrong_format():
    """При отсутствии нужных ключей взводит QuizFileWrongFormatAliceException"""
    quiz = Quiz()
    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz1_no_question.json")

    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz2_no_choices.json")

    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz3_no_correct_choice.json")


def test_load_from_file_with_wrong_correct_choice():
    """Если ключ correct_choice ошибочный, взводит QuizFileWrongAnswerAliceException"""
    quiz = Quiz()
    with pytest.raises(QuizFileWrongAnswerAliceException):
        quiz.load_questions(
            "tests/quiz_patterns/quiz4_wrong_correct_choice.json"
        )


def test_advance_question():
    """Проверка is_finished(), advance_question() и свойств
    mistakes_count, current_question_number
    """
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    assert quiz.is_finished() is False
    assert quiz.total_questions_count == 3
    assert quiz.mistakes_count == 0
    assert quiz.current_question_number == 1
    # обрабатываем первый вопрос как правильный ответ
    quiz.advance_question(is_correct_answer=True)
    assert quiz.is_finished() is False
    assert quiz.mistakes_count == 0
    assert quiz.current_question_number == 2
    # обрабатываем первый вопрос как неправильный ответ
    quiz.advance_question(is_correct_answer=False)
    assert quiz.is_finished() is False
    assert quiz.mistakes_count == 1
    assert quiz.current_question_number == 3
    # обрабатываем третий вопрос как правильный ответ
    quiz.advance_question(is_correct_answer=True)
    assert quiz.is_finished()
    assert quiz.mistakes_count == 1
    assert quiz.current_question_number == 4
    with pytest.raises(QuizIsFinishedAliceException):
        quiz.advance_question(is_correct_answer=False)


def test_load_from_file():
    """Загрузка из корректного файла викторины"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    assert quiz.total_questions_count == 3
    assert quiz.mistakes_count == 0
    assert quiz.current_question_number == 1
    assert quiz.is_finished() is False


def test_is_user_choice_correct():
    """Проверка is_user_choice_correct()"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    assert quiz.is_user_choice_correct("а")
    assert not quiz.is_user_choice_correct("б")
    assert not quiz.is_user_choice_correct("в")
    quiz.advance_question(is_correct_answer=False)
    assert not quiz.is_user_choice_correct("а")
    assert quiz.is_user_choice_correct("б")
    assert not quiz.is_user_choice_correct("в")
    quiz.advance_question(is_correct_answer=False)
    assert not quiz.is_user_choice_correct("а")
    assert not quiz.is_user_choice_correct("б")
    assert quiz.is_user_choice_correct("в")
    quiz.advance_question(is_correct_answer=True)
    with pytest.raises(QuizNoActiveQuestionAliceException):
        quiz.is_user_choice_correct("а")


def test_get_current_question():
    """Проверка _get_current_question()."""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    # тест вопроса 1 (без перемешивания)
    question_1 = quiz._get_current_question()
    assert "Текст вопроса 1?" in question_1.question
    assert question_1 == quiz._questions[0]
    quiz.advance_question(is_correct_answer=True)
    # анализ второго вопроса
    question_2 = quiz._get_current_question()
    assert "Текст вопроса 2?" in question_2.question
    assert question_2 == quiz._questions[1]
    # обрабатываем второй вопрос как не правильный ответ
    quiz.advance_question(is_correct_answer=False)
    # анализ третьего вопроса
    question_3 = quiz._get_current_question()
    assert "Текст вопроса 3?" in question_3.question
    assert question_3 == quiz._questions[2]
    # обрабатываем последний вопрос как правильный ответ
    quiz.advance_question(is_correct_answer=True)
    with pytest.raises(QuizNoActiveQuestionAliceException):
        quiz._get_current_question()


def test_get_question_and_get_current_answer():
    """Проверка get_question(), get_current_answer()"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    # тест вопроса 1 (без перемешивания)
    question_1 = quiz.get_question()
    assert "Текст вопроса 1?" in question_1
    assert (
        "Ответ 1.1" in question_1
        and "Ответ 1.2" in question_1
        and "Ответ 1.3" in question_1
    )
    answer_1 = quiz.get_current_answer()
    assert "'А') - Ответ 1.1" in answer_1
    quiz.advance_question(is_correct_answer=True)
    # анализ второго вопроса
    question_2 = quiz.get_question()
    assert "Текст вопроса 2?" in question_2
    assert (
        "Ответ 2.1" in question_2
        and "Ответ 2.2" in question_2
        and "Ответ 2.3" in question_2
    )
    answer_2 = quiz.get_current_answer()
    assert "'Б') - Ответ 2.2" in answer_2
    # обрабатываем второй вопрос как не правильный ответ
    quiz.advance_question(is_correct_answer=False)
    # анализ третьего вопроса
    question_3 = quiz.get_question()
    assert "Текст вопроса 3?" in question_3
    assert (
        "Ответ 3.1" in question_3
        and "Ответ 3.2" in question_3
        and "Ответ 3.3" in question_3
    )
    answer_3 = quiz.get_current_answer()
    assert "'В') - Ответ 3.3" in answer_3
    # обрабатываем последний вопрос как правильный ответ
    quiz.advance_question(is_correct_answer=True)
    with pytest.raises(QuizIsFinishedAliceException):
        quiz.get_question()
    with pytest.raises(QuizNoActiveQuestionAliceException):
        quiz.get_current_answer()


def test_restart():
    """Проверка restart() сбрасывает прогресс теста"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    quiz.advance_question(True)
    quiz.advance_question(True)
    quiz.advance_question(False)
    assert quiz.mistakes_count == 1
    assert quiz.current_question_number == 4
    assert quiz.is_finished()
    quiz.restart()
    assert quiz.mistakes_count == 0
    assert quiz.current_question_number == 1
    assert quiz.is_finished() is False


def test_dump_state():
    """Проверка dump_state()"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    state = quiz.dump_state()
    assert state == {
        "questions_order": [0, 1, 2],
        "current_question_number": 0,
        "mistakes_count": 0,
    }
    quiz.advance_question(False)
    state = quiz.dump_state()
    assert state == {
        "questions_order": [0, 1, 2],
        "current_question_number": 1,
        "mistakes_count": 1,
    }
    quiz.advance_question(True)
    state = quiz.dump_state()
    assert state == {
        "questions_order": [0, 1, 2],
        "current_question_number": 2,
        "mistakes_count": 1,
    }


def test_load_state():
    """Проверка load_state()"""
    quiz = Quiz()
    quiz.load_questions("tests/quiz_patterns/quiz_ok.json")
    assert quiz._current_question_number == 0
    assert quiz._mistakes_count == 0
    assert quiz._questions_order == [0, 1, 2]

    state_1 = {
        "questions_order": [2, 0, 1],
        "current_question_number": 2,
        "mistakes_count": 1,
    }
    quiz.load_state(state_1)
    assert quiz._current_question_number == 2
    assert quiz._mistakes_count == 1
    assert quiz._questions_order == [2, 0, 1]
