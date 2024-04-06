import random
from enum import IntEnum
from typing import Any

from app.constants.quiz.intents import QuizIntents
from app.constants.quiz.messages import QuizMessages
from app.core.logger_initialize import logger
from app.quiz.exceptions import QuizException
from app.quiz.quiz import Quiz
from app.settings import settings


class QuizState(IntEnum):
    """Состояния диалога викторины."""

    INIT = 0
    RULES = 1
    IN_PROGRESS = 2
    FINISHED = 3
    TERMINATED = 4
    RESUME = 5
    RESTART = 6


class QuizSkill:
    def __init__(self, filename: str = settings.QUIZ_FILE_PATH):
        """Инициализация викторины вопросами из файла filename."""
        self._quiz = Quiz()
        self._state = QuizState.INIT
        try:
            self._quiz.load_questions(filename)
            self._quiz.restart()
        except QuizException as e:
            logger.exception(e)

    def is_finished(self) -> bool:
        """Возвращает True, если работа с викториной завершена.

        Returns:
            bool: True - если викторина не начата, или прервана досрочно или
            завершена и заданы все вопросы.
        """
        return self._state in (
            QuizState.INIT,
            QuizState.FINISHED,
            QuizState.TERMINATED,
        )

    def _get_final_result(self) -> str:
        """Возвращает строку результата для завершенной викторины."""
        match self._quiz.mistakes_count:
            case 0:
                return QuizMessages.RESULT_EXCELLENT.format(
                    total=self._quiz.current_question_number - 1,
                )
            case 1:
                return QuizMessages.RESULT_GOOD_1
            case 2:
                return QuizMessages.RESULT_GOOD_2
            case 3 | 4:
                return QuizMessages.RESULT_NOT_BAD_3_4.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case 5 | 6:
                return QuizMessages.RESULT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case _:
                return QuizMessages.RESULT_VERY_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
        return ""

    def _get_partial_result(self) -> str:
        """Возвращает строку промежуточного результата прерванной викторины."""
        match self._quiz.mistakes_count:
            case 0:
                return QuizMessages.PARTIAL_RESULT_0
            case 1:
                return QuizMessages.PARTIAL_RESULT_1
            case 2:
                return QuizMessages.PARTIAL_RESULT_NOT_BAD.format(
                    mistakes="две",
                )
            case 3 | 4:
                return QuizMessages.PARTIAL_RESULT_NOT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
            case _:
                return QuizMessages.PARTIAL_RESULT_BAD.format(
                    mistakes=self._quiz.mistakes_count,
                )
        return ""

    def _get_current_result(self) -> str:
        """Возвращает строку текущего результата викторины."""
        if self._quiz.is_finished():
            return self._get_final_result() + QuizMessages.AFTER_QUIZ
        return self._get_partial_result() + QuizMessages.AFTER_QUIZ

    def _get_full_question(self) -> str:
        """Возвращает полный текст вопроса с вариантами ответов."""
        question_and_choices = self._quiz.get_question()
        return QuizMessages.FULL_QUESTION_FORMAT.format(
            current_question_number=self._quiz.current_question_number,
            question_and_choices=question_and_choices,
        )

    def _get_answer_result(self, is_correct_answer: bool) -> str:
        """Возвращает результат в зависимости от правильности ответа."""
        if is_correct_answer:
            return random.choice(QuizMessages.CORRECT_VARIANTS)
        return (
            random.choice(QuizMessages.INCORRECT_VARIANTS)
            + self._quiz.get_current_answer()
        )

    def dump_state(self):
        """Возвращает словарь текущего состояния.

        Returns:
            dict() - словарь текущего состояния вида::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int,
                "state": int
            }
        """
        state = self._quiz.dump_state()
        state["state"] = int(self._state)
        return state

    def load_state(self, state: dict[str, str] | None):
        """Загружает информацию о состоянии викторины из словаря.

        Args:
            state - словарь сохраненного состояния вида::

            {
                "questions_order": list[int],
                "current_question_number": int,
                "mistakes_count": int,
                "state": int
            }
        """
        if not state:
            self._quiz.restart()
            self._state = QuizState.INIT
            return
        state_tmp = state.copy()
        if "state" in state_tmp:
            self._state = QuizState(state_tmp.pop("state"))
        self._quiz.load_state(state_tmp)

    def _process_init_state(
        self,
        *args,
    ) -> tuple[bool, str]:
        """Обработчик начального запуска до показа правил."""
        self._state = QuizState.RULES
        return True, QuizMessages.RULES.format(
            total_questions_count=self._quiz.total_questions_count,
        )

    def _process_rules_state(
        self,
        intents: dict[str:Any],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик первоначального показа правил."""
        if QuizIntents.TAKE_QUIZ in intents or QuizIntents.REPEAT in intents:
            # повторить правила
            return True, QuizMessages.RULES.format(
                total_questions_count=self._quiz.total_questions_count,
            )
        if QuizIntents.TERMINATE_QUIZ in intents:
            # выход до показа первого вопроса
            self._state = QuizState.INIT
            return True, QuizMessages.NO_RESULTS + QuizMessages.AFTER_QUIZ
        if QuizIntents.AGREE in intents or QuizIntents.CONFIRM in intents:
            # получено согласие на запуск викторины
            self._state = QuizState.IN_PROGRESS
            if not self._quiz.is_finished():
                return True, self._get_full_question()
            return True, QuizMessages.NO_QUIZ
        # return False, QuizMessages.UNKNOWN_COMMAND
        # при нераспознанной команде подсказка для выбора
        return True, QuizMessages.RULES_CHOICES

    def _process_in_progress_state(
        self,
        intents: dict[str:Any],
        command: str,
    ) -> tuple[bool, str]:
        """Обработчик в режиме прогресса викторины."""
        if QuizIntents.REPEAT in intents:
            # повторить последний вопрос
            return True, self._get_full_question()
        if QuizIntents.NO_ANSWER in intents:
            # нет ответа - подбодрить
            return True, random.choice(QuizMessages.CHEER_UP_VARIANTS)
        if QuizIntents.TERMINATE_QUIZ in intents:
            # досрочно завершить викторину
            self._state = QuizState.TERMINATED
            return True, self._get_current_result()
        if command in ["а", "б", "в"]:
            # обработка ответа
            is_correct_answer = self._quiz.is_user_choice_correct(command)
            answer_result = self._get_answer_result(is_correct_answer)
            self._quiz.advance_question(is_correct_answer)
            if self._quiz.is_finished():
                self._state = QuizState.FINISHED
                answer_result += (
                    QuizMessages.IS_FINISHED + self._get_current_result()
                )
            else:
                answer_result += self._get_full_question()
            return True, answer_result
        # неизвестный вариант ответа - показать подсказку
        return True, QuizMessages.CHOICE_HELP

    def _process_finished_state(
        self,
        *args,
    ) -> tuple[bool, str]:
        """Обработчик в режиме завершенной викторины."""
        # викторина уже завершена
        self._state = QuizState.RESTART
        result = " ".join(
            [
                QuizMessages.ALREADY_FINISHED,
                self._get_final_result(),
                QuizMessages.RESET_PROGRESS,
            ],
        )
        return True, result

    def _process_restart_state(
        self,
        intents: dict[str:Any],
        command: str,
    ) -> tuple[bool, str]:
        """Обработчик диалога викторины 'начать заново'."""
        if (
            QuizIntents.START_AGAIN in intents
            or QuizIntents.CONFIRM in intents
        ):
            # запустить заново
            self._state = QuizState.RULES
            self._quiz.restart()
            return True, QuizMessages.RULES.format(
                total_questions_count=self._quiz.total_questions_count,
            )
        if (
            QuizIntents.REJECT in intents
            or QuizIntents.TERMINATE_QUIZ in intents
        ):
            self._state = QuizState.FINISHED
            return True, QuizMessages.NO_RESULTS

        return True, " ".join(
            [
                QuizMessages.ALREADY_FINISHED,
                self._get_final_result(),
                QuizMessages.RESET_PROGRESS,
            ],
        )

    def _process_terminated_state(
        self,
        intents: dict[str:Any],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик досрочно завершенной викторины."""
        if QuizIntents.TAKE_QUIZ in intents:
            # викторина уже завершена
            self._state = QuizState.RESUME
            return True, QuizMessages.ALREADY_IN_PROGRESS.format(
                current_question_number=self._quiz.current_question_number,
            )
        return False, ""

    def _process_resume_state(
        self,
        intents: dict[str:Any],
        *args,
    ) -> tuple[bool, str]:
        """Обработчик диалога возобновления викторины."""
        if QuizIntents.REPEAT in intents:
            # повторить диалог возобновления викторины
            return True, QuizMessages.RESUME_REPEAT.format(
                current_question_number=self._quiz.current_question_number,
            )
        if QuizIntents.START_AGAIN in intents:
            # запустить заново
            self._quiz.restart()
            self._state = QuizState.IN_PROGRESS
            return True, self._get_full_question()
        if QuizIntents.CONTINUE in intents:
            # продолжить
            self._state = QuizState.IN_PROGRESS
            return True, self._get_full_question()
        if QuizIntents.TERMINATE_QUIZ in intents:
            # досрочно завершить викторину
            self._state = QuizState.TERMINATED
            return True, self._get_current_result()
        # повторить диалог возобновления викторины
        return True, QuizMessages.RESUME_REPEAT.format(
            current_question_number=self._quiz.current_question_number,
        )

    def execute_command(
        self,
        command: str,
        intents: dict[str:Any],
    ) -> tuple[bool, str]:
        """Анализ и исполнение команды/интента.

        Args:
            command (str): Команда для навыка.
            intents (dict[str]): Словарь намерений (intents) для навыка.

        Returns:
            (result, answer): Кортеж ответа, где.
            result (bool): True, если команда воспринята викториной.
            answer (str): Текстовое сообщение ответа на команду.
        """
        command = command.lower()
        state_processors = {
            QuizState.INIT: self._process_init_state,
            QuizState.RULES: self._process_rules_state,
            QuizState.IN_PROGRESS: self._process_in_progress_state,
            QuizState.FINISHED: self._process_finished_state,
            QuizState.TERMINATED: self._process_terminated_state,
            QuizState.RESUME: self._process_resume_state,
            QuizState.RESTART: self._process_restart_state,
        }
        if self._state in state_processors:
            return state_processors[self._state](intents, command)
        return False, ""
