from icecream import ic

from app.constants.comands_states_answers import (
    COMMANDS_STATES_ANSWERS_INTENTS,
    ORDERED_STATES,
    another_answers_documents,
)
from app.constants.commands import ServiceCommands
from app.constants.states import (
    CORE_STATES,
    STATE_HELP_MAIN,
    STATES,
    STATES_BY_GROUP,
)
from app.core.utils import (
    compose_message,
    disagree_answer_by_state,
    find_previous_state,
    get_after_answer_by_state,
    get_answer_by_state,
    get_disagree_answer_by_state,
    get_states_by_order,
    get_states_group_by_state,
    last_states,
    next_state,
)
from app.manual_training_player.manual_training_player import (
    ManualTrainingPlayer,
)
from app.quiz.quizskill import QuizSkill

QUIZ_SESSION_STATE_KEY = "quiz_state"


class FiniteStateMachine:
    """Класс навыка.

    Определяет правила перехода между состояниями навыка.

    Attributes:
        message(str): Сообщение, которое зачитывает Алиса.
        progress(list[str]): Прогресс прохождения всех историй в навыке.
        incorrect_answers(int): Количество неправильных ответов.
        command(str): Команда пользователя.
        is_to_progress(boolean): Флаг согласия/отказа.
        max_progress(int): Максимальное количество состояний навыка.
        quiz_skill: Объект `QuizSkill` (викторина).
        manual_training: Объект `AudioAssistant` (аудио-плеер).
    """

    def __init__(self):
        self.message = ""
        self.progress = []
        self.history = []
        self.incorrect_answers = 0
        self.command = ""
        self.previous_command = ""
        self.is_to_progress = False
        self.max_progress = len(STATES) - 1
        self.quiz_skill = QuizSkill()
        self.manual_training = ManualTrainingPlayer()

    def is_agree(self) -> bool:
        """Функция состояния.

        Проверяет, ответил ли пользователь согласием.

        Returns:
            True, если пользователь согласился.
        """
        return self.command in ServiceCommands.AGREE

    def is_disagree(self):
        """Функция состояния.

        Проверяет, ответил ли пользователем отказом.

        Returns:
            True, если пользователь отказался.
        """
        return self.command in ServiceCommands.DISAGREE

    def action_func(self, state_name: str) -> callable:
        """Флаг согласия/отказа.

        Args:
            state_name: Название состояния.
            self: Объект FiniteStateMachine.
        """

        if self.is_disagree():
            self.disagree_function(state_name)
        else:
            self.agree_function(state_name)

    def save_progress(self, current_step: str) -> None:
        """Прогресс прохождения навыка.

        Сохраняет состояние прохождения навыка.

        Args:
            self: Объект FiniteStateMachine.
            current_step: Состояние навыка.
        """
        if self.is_to_progress and current_step in STATES[1:]:
            self.progress = list(set(self.progress) - {current_step}) + [
                current_step,
            ]
            self.is_to_progress = False

    def save_history(self, current_step: str) -> None:
        """История прохождения навыка.

        Сохраняет состояние прохождения навыка. Включает в себя состояния
        в которых прогресс не записывается (отрицательный ответ пользователя)

        Note:
            Используется для генерации подходящих отрицательных ответов.

        Args:
            current_step: Текущее состояние.
        """
        self.history = list(set(self.progress) - {current_step}) + [
            current_step,
        ]

    def agree_function(self, state):
        """Вызывается при положительном ответе пользователя.

        Положительный ответ включает в себя прямой вызов команды.

        Args:
            state: Вызванное состояние.
        """
        self.save_progress(state)
        self.save_history(state)
        ic(self.history, self.progress)
        answer = self._get_answer(state)
        after_answer = self._get_after_answer(state)
        self.message = compose_message(answer, after_answer)
        self.incorrect_answers = 0

    def disagree_function(self, state: str) -> None:
        """Соответствует отказу пользователя.

        Args:
            state: Состояние, в которое переходим.
        """
        self.save_progress(state)
        if state in CORE_STATES:
            self.history.extend(
                get_states_group_by_state(
                    state,
                    STATES_BY_GROUP,
                ),
            )
        else:
            self.save_history(state)
        disagree_answer = self.get_next_disagree_answer(
            state,
        )
        self.message = disagree_answer
        self.incorrect_answers = 0

    def _get_answer(self, state: str) -> str:
        """Генерирует основной ответ навыка по состоянию.

        Args:
            state: Состояние, по которому генерируем ответ.

        Returns:
            Ответ навыка.
        """
        if self._is_repeat_and_previous_disagree():
            return disagree_answer_by_state(
                state,
                COMMANDS_STATES_ANSWERS_INTENTS,
            )
        return get_answer_by_state(
            state,
            COMMANDS_STATES_ANSWERS_INTENTS,
        )

    def _get_after_answer(self, state: str) -> str:
        """Генерирует вторую часть ответа с подсказкой о продолжении.

        Args:
            state: Триггер, по которому генерируем подсказку.

        Returns:
            Подсказка.
        """
        if self.is_agree() and not self._is_repeat_and_previous_disagree():
            return get_after_answer_by_state(
                state,
                COMMANDS_STATES_ANSWERS_INTENTS,
            )
        if not self._is_repeat_and_previous_disagree():
            return self.get_next_after_answer(state)
        return ""

    def _is_repeat_and_previous_disagree(self) -> bool:
        """Проверка.

        Является ли команда пользователя командой повтора и предыдущая
        команда - командой отказа.

        Returns:
            True, если команда повтора и отказа.
        """
        return (
            self.command == ServiceCommands.REPEAT
            and self.previous_command in ServiceCommands.DISAGREE
        )

    def get_next_after_answer(self, step: str) -> str:
        """Возвращает следующий ответ с подсказкой для пользователя.

        Args:
            step: Текущее состояние.

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        while step in self.progress:
            step = self.next_state_by_history(
                COMMANDS_STATES_ANSWERS_INTENTS,
            )
        # исправляем side effect, когда в помощи появляется `after_answer`
        if step == STATE_HELP_MAIN:
            return ""
        pre_step = find_previous_state(step, ORDERED_STATES)
        return get_after_answer_by_state(
            pre_step,
            COMMANDS_STATES_ANSWERS_INTENTS,
        )

    def get_next_disagree_answer(self, step: str) -> str:
        """Возвращает следующий ответ с вариантами действия пользователя.

        Args:
            step: Текущее состояние.

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        while step in self.history:
            step = next_state(
                step,
                ORDERED_STATES,
            )
        return get_disagree_answer_by_state(
            self.history[-1],
            COMMANDS_STATES_ANSWERS_INTENTS,
        )

    def dont_understand(self) -> str:
        """Обработка ответов, когда система не понимает пользователя.

        Увеличивает счетчик ответов и устанавливает сообщение
        в зависимости от счетчика.
        """
        self.incorrect_answers += 1
        if self.incorrect_answers <= 1:
            return another_answers_documents.get(
                "dont_understand_the_first_time",
                "",
            )
        return another_answers_documents.get(
            "dont_understand_more_than_once",
            "",
        )

    def dump_session_state(self) -> dict:
        """Функция возвращает словарь ответа для сохранения состояния навыка.

        Returns:
            словарь сохраненного состояния вида.

        Examples:
            {
                "quiz_state": {....} - параметры состояния викторины
                ...
            }
        """
        # state["test_value"] = 123
        # тут добавляем другие ключи для других разделов,
        # если нужно что-то хранить, например текущее состояние
        return {QUIZ_SESSION_STATE_KEY: self.quiz_skill.dump_state()}

    def load_session_state(self, session_state: dict) -> None:
        """Загружает текущее состояние из словаря session_state."""
        quiz_state = None
        if QUIZ_SESSION_STATE_KEY in session_state:
            quiz_state = session_state.pop(QUIZ_SESSION_STATE_KEY)
        self.quiz_skill.load_state(quiz_state)
        # тут возможна загрузка других ключей при необходимости

    def is_completed(self) -> bool:  # noqa
        """Проверяет, завершено ли обучение.

        Обучение считается завершенным, когда выполнены все элементы навыка.

        Returns:
            True, если все элементы навыка завершены, иначе False.
        """
        try:
            result = len(self.progress) == self.max_progress
        except TypeError:
            result = False
        return result

    def next_state_by_history(
        self,
        states: list,
    ) -> str:
        """Возвращает следующее состояние.

        Очередность определяется списком состояний STATES в states.py.
        Учитывается прогресс пользователя.

        Args:
            states: Список всех триггеров.

        Returns:
            Триггер, соответствующий первой непройденной истории/возможности
            после последнего выполненного действия.
        """
        state = last_states(self.history)
        ordered_states = get_states_by_order(states)
        if state is None:
            return ordered_states[0]
        state_index = ordered_states.index(state)
        len_states = len(ordered_states)
        for index in range(state_index, len_states + state_index):
            if ordered_states[index % len_states] in self.history:
                continue
            return ordered_states[index % len_states]

    def get_output(
        self,
        answer_text,
        directives=None,
        end_session=False,
    ) -> dict[str, str]:
        """Функция возвращает словарь с ответом и дополнительными данными.

        Args:
            answer_text: Текст ответа.
            directives: Команды для аудиоплеера.
            end_session: Ключ для завершения сессии.
        """
        return {
            "response": {
                "text": answer_text,
                "end_session": end_session,
                "directives": directives,
            },
            "session_state": self.dump_session_state(),
            "version": "1.0",
        }
