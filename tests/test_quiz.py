import json

import pytest

from app.constants.quiz.intents import Intents
from app.quiz import (
    Quiz,
    QuizFileNotFoundAliceException,
    QuizFileWrongAnswerAliceException,
    QuizFileWrongFormatAliceException,
    QuizIsFinishedAliceException,
    QuizNoActiveQuestionAliceException,
    QuizSkill,
    QuizState,
)

quiz_state_init = {
    "questions_order": [0, 1, 2],
    "current_question_number": 0,
    "mistakes_count": 0,
    "state": int(QuizState.INIT),
}

quiz_state_rules = {
    "questions_order": [0, 1, 2],
    "current_question_number": 0,
    "mistakes_count": 0,
    "state": int(QuizState.RULES),
}

quiz_state_in_progress = {
    "questions_order": [2, 1, 0],
    "current_question_number": 2,
    "mistakes_count": 1,
    "state": int(QuizState.IN_PROGRESS),
}

quiz_state_in_progress_0 = {
    "questions_order": [2, 1, 0],
    "current_question_number": 0,
    "mistakes_count": 0,
    "state": int(QuizState.IN_PROGRESS),
}

quiz_state_finished = {
    "questions_order": [2, 1, 0],
    "current_question_number": 3,
    "mistakes_count": 1,
    "state": int(QuizState.FINISHED),
}

quiz_state_terminated = {
    "questions_order": [2, 1, 0],
    "current_question_number": 2,
    "mistakes_count": 1,
    "state": int(QuizState.TERMINATED),
}

quiz_state_resume = {
    "questions_order": [2, 1, 0],
    "current_question_number": 2,
    "mistakes_count": 1,
    "state": int(QuizState.RESUME),
}

quiz_skill_state_fixtures = [
    quiz_state_init,
    quiz_state_rules,
    quiz_state_in_progress_0,
    quiz_state_in_progress,
    quiz_state_finished,
    quiz_state_terminated,
    quiz_state_resume,
]


def test_load_from_wrong_file_name():
    """Загрузка из отсутствующего файла взводит
    QuizFileNotFoundAliceException.
    """
    quiz = Quiz()
    with pytest.raises(QuizFileNotFoundAliceException):
        quiz.load_questions("wrong_file_name.json")


def test_load_from_file_wrong_format():
    """При отсутствии нужных ключей взводит
    QuizFileWrongFormatAliceException.
    """
    quiz = Quiz()
    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz1_no_question.json")
    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz2_no_choices.json")
    with pytest.raises(QuizFileWrongFormatAliceException):
        quiz.load_questions("tests/quiz_patterns/quiz3_no_correct_choice.json")


def test_load_from_file_with_wrong_correct_choice():
    """Если ключ correct_choice ошибочный, взводит
    QuizFileWrongAnswerAliceException.
    """
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
    assert "Ответ 1.1" in answer_1
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
    assert "Ответ 2.2" in answer_2
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
    assert "Ответ 3.3" in answer_3
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


def test_quiz_skill_init():
    """Проверка инициализации викторины вопросами из заданного файла."""
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    assert quiz_skill._state == QuizState.INIT
    assert quiz_skill._quiz.current_question_number == 1
    assert quiz_skill._quiz.mistakes_count == 0
    assert quiz_skill._quiz.total_questions_count == 3


@pytest.mark.parametrize("state", quiz_skill_state_fixtures)
def test_quiz_skill_load_dump_state(state: dict[str]):
    """Проверка load_state(), dump_state()"""
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    state_json = json.dumps(state, sort_keys=True)
    quiz_skill.load_state(state)
    dump_json = json.dumps(quiz_skill.dump_state(), sort_keys=True)
    assert state_json == dump_json


def test_quiz_skill_init_transitions():
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_init)
    quiz_skill.execute_command("", {})
    assert quiz_skill._state == QuizState.RULES, "Ошибка перехода INIT>RULES"


@pytest.mark.parametrize(
    "intent, new_state, expected_result",
    [
        (Intents.REPEAT, QuizState.RULES, True),
        (Intents.TERMINATE_QUIZ, QuizState.INIT, True),
        (Intents.AGREE, QuizState.IN_PROGRESS, True),
        ("unknown_intent", QuizState.RULES, False),
    ],
)
def test_quiz_skill_rules_transitions(
    intent: str,
    new_state: QuizState,
    expected_result: bool,
):
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_rules)
    result, msg = quiz_skill.execute_command("", {intent: "any"})
    assert result == expected_result
    assert (
        quiz_skill._state == new_state
    ), f"Ошибка перехода из RULES по команде {intent}"


@pytest.mark.parametrize(
    "command, intent, new_state, expected_result",
    [
        ("", Intents.REPEAT, QuizState.IN_PROGRESS, True),
        ("", Intents.NO_ANSWER, QuizState.IN_PROGRESS, True),
        ("", Intents.TERMINATE_QUIZ, QuizState.TERMINATED, True),
        ("а", "а", QuizState.FINISHED, True),
        ("unknown_command", "unknown_intent", QuizState.IN_PROGRESS, True),
    ],
)
def test_quiz_skill_in_progress_transitions(
    command: str,
    intent: str,
    new_state: QuizState,
    expected_result: bool,
):
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_in_progress)
    result, msg = quiz_skill.execute_command(command, {intent: "any"})
    assert result == expected_result
    assert (
        quiz_skill._state == new_state
    ), f"Ошибка перехода из IN_PROGRESS по команде {intent}"


def test_quiz_skill_in_progress_flow():
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_in_progress_0)
    assert quiz_skill._quiz.current_question_number == 1
    # верный ответ
    result, _ = quiz_skill.execute_command("в", {})
    assert result
    assert quiz_skill._quiz.mistakes_count == 0
    assert quiz_skill._quiz.current_question_number == 2
    assert quiz_skill._state == QuizState.IN_PROGRESS
    # неверный ответ
    result, _ = quiz_skill.execute_command("в", {})
    assert result
    assert quiz_skill._quiz.mistakes_count == 1
    assert quiz_skill._quiz.current_question_number == 3
    assert quiz_skill._state == QuizState.IN_PROGRESS
    # неверный ответ
    result, _ = quiz_skill.execute_command("в", {})
    assert result
    assert quiz_skill._quiz.mistakes_count == 2
    assert quiz_skill._quiz.current_question_number == 4
    assert quiz_skill._state == QuizState.FINISHED


@pytest.mark.parametrize(
    "intent, new_state, expected_result",
    [
        (Intents.TAKE_QUIZ, QuizState.FINISHED, True),
        (Intents.START_AGAIN, QuizState.RULES, True),
        ("unknown_intent", QuizState.FINISHED, False),
    ],
)
def test_quiz_skill_finished_transitions(
    intent: str,
    new_state: QuizState,
    expected_result: bool,
):
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_finished)
    result, _ = quiz_skill.execute_command("", {intent: "any"})
    assert result == expected_result
    assert (
        quiz_skill._state == new_state
    ), f"Ошибка перехода из FINISHED по команде {intent}"


@pytest.mark.parametrize(
    "intent, new_state, expected_result",
    [
        (Intents.TAKE_QUIZ, QuizState.RESUME, True),
        ("unknown_intent", QuizState.TERMINATED, False),
    ],
)
def test_quiz_skill_terminated_transitions(
    intent: str,
    new_state: QuizState,
    expected_result: bool,
):
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_terminated)
    result, _ = quiz_skill.execute_command("", {intent: "any"})
    assert result == expected_result
    assert (
        quiz_skill._state == new_state
    ), f"Ошибка перехода из TERMINATED по команде {intent}"


@pytest.mark.parametrize(
    "intent, new_state, expected_result",
    [
        (Intents.REPEAT, QuizState.RESUME, True),
        (Intents.START_AGAIN, QuizState.IN_PROGRESS, True),
        (Intents.CONTINUE, QuizState.IN_PROGRESS, True),
        (Intents.TERMINATE_QUIZ, QuizState.TERMINATED, True),
        ("unknown_intent", QuizState.RESUME, True),
    ],
)
def test_quiz_skill_resume_transitions(
    intent: str,
    new_state: QuizState,
    expected_result: bool,
):
    quiz_skill = QuizSkill(filename="tests/quiz_patterns/quiz_ok.json")
    quiz_skill.load_state(quiz_state_resume)
    result, _ = quiz_skill.execute_command("", {intent: "any"})
    assert result == expected_result
    assert (
        quiz_skill._state == new_state
    ), f"Ошибка перехода из RESUME по команде {intent}"
