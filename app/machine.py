from app.constants.comands_states_answers import (
    COMMANDS_STATES_ANSWERS_INTENTS,
    HELP_COMMANDS,
    HELP_COMMANDS_STATES_ANSWERS_INTENTS,
    ORDERED_STATES,
    another_answers_documents,
)
from app.constants.commands import ServiceCommands
from app.constants.intents import INTENTS, ServiceIntents
from app.constants.states import CORE_STATES, STATES, STATES_BY_GROUP
from app.core.exceptions import StateDumpError, StateLoadError
from app.core.utils import (
    compose_message,
    disagree_answer_by_state,
    find_previous_state,
    get_after_answer_by_state,
    get_answer_by_state,
    get_disagree_answer_by_state,
    get_last_in_history,
    get_states_by_order,
    get_states_group_by_state,
    last_states,
)
from app.manual_training_player.manual_training_player import (
    ManualTrainingPlayer,
)
from app.quiz.quizskill import QuizSkill
from app.schemas import InnerResponse, ResponseData

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
        self.intents = {}
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
        return (
            self.command in ServiceCommands.AGREE
            or ServiceIntents.AGREE in self.intents
        )

    def is_disagree(self) -> bool:
        """Функция состояния.

        Проверяет, ответил ли пользователем отказом.

        Returns:
            True, если пользователь отказался.
        """
        return (
            self.command in ServiceCommands.DISAGREE
            or ServiceIntents.DISAGREE in self.intents
            or ServiceIntents.NEXT in self.intents
        )

    def action_func(self, state_name: str) -> callable:
        """Функция действия.

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
        answer = self.get_answer(state)
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
        disagree_answer = self.get_next_disagree_answer()
        self.message = disagree_answer
        self.incorrect_answers = 0

    def get_answer(self, state: str) -> str:
        """Генерирует основной ответ навыка по состоянию.

        Args:
            state: Состояние, по которому генерируем ответ.

        Returns:
            Ответ навыка.
        """
        if self.command in HELP_COMMANDS or INTENTS.get_help_available(
            self.intents,
        ):
            structure = HELP_COMMANDS_STATES_ANSWERS_INTENTS
        else:
            structure = COMMANDS_STATES_ANSWERS_INTENTS
        if self._is_repeat_and_previous_disagree():
            return disagree_answer_by_state(
                state,
                structure,
            )
        return get_answer_by_state(
            state,
            structure,
        )

    def _get_after_answer(self, state: str) -> str:
        """Генерирует вторую часть ответа с подсказкой о продолжении.

        Args:
            state: состояние, по которому генерируем подсказку.

        Returns:
            Подсказка.
        """
        if self.is_completed():
            self.progress = []
            self.history = []
            return another_answers_documents.get("all_completed")
        if self.is_agree() and not self._is_repeat_and_previous_disagree():
            return self.get_next_after_answer(
                state,
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
        pre_step = find_previous_state(step, ORDERED_STATES)
        return get_after_answer_by_state(
            pre_step,
            COMMANDS_STATES_ANSWERS_INTENTS,
        )

    def get_next_disagree_answer(
        self,
    ) -> str:
        """Возвращает следующий ответ с вариантами действия пользователя.

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        return get_disagree_answer_by_state(
            get_last_in_history(self.history),
            COMMANDS_STATES_ANSWERS_INTENTS,
        )

    def _dump_states(
        self,
        states: list[str],
        ordered_states: list[str],
    ) -> list[int]:
        """Формирование списка номеров состояний для сохранения в сессии.

        Args:
            states: Список состояний навыка (history или progress).
            ordered_states: Упорядоченный список состояний.

        Raises:
            StateDumpError: Если в states обнаружено состояние,
                отсутствующее в ordered_states.

        Returns:
            Упорядоченный список, в котором каждое из состояний states
            заменено соответствующим индексом этого состояния в ordered_states.
        """
        result = []
        for state in states:
            try:
                result.append(ordered_states.index(state))
            except ValueError:
                # logger.error(
                #     f"Ошибка сохранения: неизвестное состояние {state}"
                # )
                raise StateDumpError(
                    f"Ошибка сохранения: неизвестное состояние {state}",
                )
        return result

    def _load_states(
        self,
        state_indexes: list[int],
        ordered_states: list[str],
    ) -> list[str]:
        """Формирование списка состояний после загрузки из сессии.

        Args:
            state_indexes: Список номеров состояний из сессии.
            ordered_states: Упорядоченный список состояний.

        Raises:
            StateLoadError: Если в state_index обнаружен index,
                выходящий за пределы ordered_states.

        Returns:
            Упорядоченный список, в котором каждое из значений states_indexes
            заменено соответствующим состоянием из ordered_states.
        """
        result = []
        for index in state_indexes:
            try:
                result.append(ordered_states[index])
            except ValueError:
                # logger.error(
                #     f"Ошибка загрузки: ошибка индекса состояния {index}"
                # )
                raise StateLoadError(
                    f"Ошибка загрузки: ошибка индекса состояния {index}",
                )
        return result

    def dump_session_state(self) -> dict:
        """Функция возвращает словарь ответа для сохранения состояния навыка.

        Returns:
            словарь сохраненного состояния вида.

        Examples:
            {
                "quiz_state": {...} - параметры состояния викторины
                "progress": []  - индексы состояний прогресса
                "history": []  - индексы состояний истории
                "training": {...} - параметры состояния обучения (плеер)
            }
        """
        # тут добавляем другие ключи для других разделов,
        # если нужно что-то хранить, например текущее состояние
        return {
            QUIZ_SESSION_STATE_KEY: self.quiz_skill.dump_state(),
            "progress": self._dump_states(self.progress, ORDERED_STATES),
            "history": self._dump_states(self.history, ORDERED_STATES),
            "training": self.manual_training.dump_state(),
            "previous_command": self.previous_command,
            "incorrect_answers": self.incorrect_answers,
        }

    def load_session_state(self, session_state: dict) -> None:
        """Загружает текущее состояние из словаря session_state."""
        quiz_state = None
        if QUIZ_SESSION_STATE_KEY in session_state:
            quiz_state = session_state.pop(QUIZ_SESSION_STATE_KEY)
        self.quiz_skill.load_state(quiz_state)
        self.incorrect_answers = session_state.get("incorrect_answers", 0)
        # тут возможна загрузка других ключей при необходимости
        dumped_progress = session_state.get("progress", [])
        self.progress = self._load_states(dumped_progress, ORDERED_STATES)
        dumped_history = session_state.get("history", [])
        self.history = self._load_states(dumped_history, ORDERED_STATES)
        self.previous_command = session_state.get("previous_command", "")
        self.manual_training.load_state(session_state.get("training"))

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
        structure: list[tuple[str, str, str, str, str, str]],
    ) -> str:
        """Возвращает следующее состояние.

        Очередность определяется списком состояний STATES в states.py.
        Учитывается прогресс пользователя.

        Args:
            structure: Список всех состояний.

        Returns:
            Состояние, соответствующее первой непройденной истории/возможности
            после последнего выполненного действия.
        """
        state = last_states(self.history)
        ordered_states = get_states_by_order(structure)
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
        should_listen=None,
    ) -> ResponseData:
        """Возвращает модель с ответом и дополнительными данными.

        Args:
            answer_text: Текст ответа.
            directives: Команды для аудиоплеера.
            end_session: Ключ для завершения сессии.
            should_listen: false для запуска плеера без ожидания запроса
            пользователя
        """
        if answer_text is None:
            answer_text = " "
        return ResponseData(
            response=InnerResponse(
                text=answer_text,
                end_session=end_session,
                should_listen=should_listen,
                directives=directives,
            ),
            session_state=self.dump_session_state(),
            version="1.0",
        )
