import logging

from transitions import Machine

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
    ORDERED_TRIGGERS,
)
from app.constants.commands import ServiceCommands
from app.constants.skill_transitions import transitions
from app.constants.states import (
    CORE_TRIGGERS,
    HELP_STATES,
    STATES,
    TRIGGERS_BY_GROUP,
)
from app.quiz import QuizSkill
from app.utils import (
    create_trigger,
    find_previous_element,
    get_after_answer_by_trigger,
    get_answer_by_trigger,
    get_disagree_answer_by_trigger,
    get_triggers_group_by_trigger,
    next_trigger,
    next_trigger_by_progress,
)

QUIZ_SESSION_STATE_KEY = "quiz_state"

logging.basicConfig(level=logging.INFO)


class FiniteStateMachine:
    """Класс навыка.

    Определяет правила перехода между состояниями навыка.

    Attributes:
        message(str): Сообщение, которое зачитывает Алиса.
        progress(list[str]): Прогресс прохождения всех историй в навыке.
        incorrect_answers(int): Количество неправильных ответов.
        command(str): Команда пользователя (в дальнейшем заменим на интенты).
        machine(Machine): Машина состояний навыка.
        flag(boolean): Флаг согласия/отказа.
        max_progress(int): Максимальное количество состояний навыка.
        quiz_skill: Объект `QuizSkill` (викторина).
    """

    def __init__(self):
        self.message = ""
        self.progress = []
        self.history = []
        self.incorrect_answers = 0
        self.command = ""
        self.machine = Machine(
            model=self,
            states=STATES + HELP_STATES,
            transitions=transitions,
            initial="start",
        )
        self.flag = False
        self.max_progress = len(STATES) - 1
        self._create_agree_functions()
        self._create_disagree_functions()
        self.quiz_skill = QuizSkill()

    def _save_progress(self, current_step: str) -> None:
        """Прогресс прохождения навыка.

        Сохраняет состояние прохождения навыка.

        Args:
            self: Объект FiniteStateMachine.
            current_step: Состояние навыка.
        """
        if self.flag and current_step in [
            create_trigger(state) for state in STATES[1:]
        ]:
            self.progress = list(set(self.progress) - {current_step}) + [
                current_step,
            ]
            self.flag = False

    def _save_history(self, current_step: str) -> None:
        """История прохождения навыка.

        Сохраняет состояние прохождения навыка. Включает в себя состояния
        в которых прогресс не записывается (отрицательный ответ пользователя)

        Note:
            Используется для генерации подходящих отрицательных ответов.

        Args:
            current_step: Текущее состояние (соответствующий триггер).
        """
        self.history = list(set(self.progress) - {current_step}) + [
            current_step,
        ]

    def _generate_agree_function(self, name, trigger):
        """Создает функции, вызываемые триггерами.

        Создаем сразу все функции, которые указаны в transitions класса
        FiniteStateMachine.
        Args:
            name: Имя функции.
            trigger: Вызванная триггер.
        """

        def _func():
            self._save_progress(trigger)
            self._save_history(trigger)
            if self.is_agree():
                after_answer = get_after_answer_by_trigger(
                    trigger,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                )
                answer = get_answer_by_trigger(
                    trigger,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                )
            else:
                after_answer = self.get_next_after_answer(trigger)
                answer = get_answer_by_trigger(
                    trigger,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                )
            self.message = answer + " " + after_answer
            self.incorrect_answers = 0

        setattr(self, name, _func)

    def _generate_disagree_function(self, name, trigger):
        """Создает функции, вызываемые триггерами."""

        def _func():
            self._save_history(trigger)
            if trigger in CORE_TRIGGERS:
                self.history.extend(
                    get_triggers_group_by_trigger(
                        trigger,
                        TRIGGERS_BY_GROUP,
                    ),
                )
            else:
                self._save_history(trigger)
            disagree_answer = self.get_next_disagree_answer(
                trigger,
            )
            self.message = disagree_answer
            self.incorrect_answers = 0

        setattr(self, name, _func)

    def _create_agree_functions(self) -> None:
        """Создание функций, обрабатывающих согласие пользователя."""
        [
            self._generate_agree_function(
                func_name,
                trigger,
            )
            for (
                command,
                trigger,
                func_name,
                answer,
                _,
                _,
            ) in COMMANDS_TRIGGERS_GET_FUNC_ANSWERS
        ]

    def _create_disagree_functions(self) -> None:
        """Создание функций, обрабатывающих отказы пользователя."""
        [
            self._generate_disagree_function(
                func_name + "_disagree",
                trigger,
            )
            for (
                command,
                trigger,
                func_name,
                _,
                _,
                disagree_answer,
            ) in COMMANDS_TRIGGERS_GET_FUNC_ANSWERS
        ]

    def get_next_after_answer(self, step: str) -> str:
        """Возвращает следующий ответ с вариантами действия пользователя.

        Args:
            step: Текущее состояние (соответствующий триггер).

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        while step in self.progress:
            step = next_trigger_by_progress(
                self,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        pre_step = find_previous_element(step, ORDERED_TRIGGERS)
        return get_after_answer_by_trigger(
            pre_step,
            COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
        )

    def get_next_disagree_answer(self, step: str) -> str:
        """Возвращает следующий ответ с вариантами действия пользователя.

        Args:
            step: Текущее состояние (соответствующий триггер).

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        while step in self.history:
            step = next_trigger(
                step,
                ORDERED_TRIGGERS,
            )
        return get_disagree_answer_by_trigger(
            step,
            COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
        )

    def dont_understand(self) -> str:
        """Обработка ответов, когда система не понимает пользователя.

        Увеличивает счетчик ответов и устанавливает сообщение
        в зависимости от счетчика.
        """
        self.incorrect_answers += 1
        if self.incorrect_answers <= 1:
            self.message = Answers.DONT_UNDERSTAND_THE_FIRST_TIME
        else:
            self.message = Answers.DONT_UNDERSTAND_MORE_THAN_ONCE
        return self.message

    def dump_session_state(self) -> dict:
        """Функция возвращает словарь ответа для сохранения состояния навыка.

        Returns:
            словарь сохраненного состояния вида.

        Examples:
            {
                "quiz_state": { .... } - параметры состояния викторины
                ...
            }
        """
        # state["test_value"] = 123
        # тут добавляем другие ключи для других разделов,
        # если нужно что-то хранить, например текущее состояние
        return {QUIZ_SESSION_STATE_KEY: self.quiz_skill.dump_state()}

    def load_session_state(self, session_state: dict):
        """Функция загружает текущее состояние из словаря session_state."""
        quiz_state = None
        if QUIZ_SESSION_STATE_KEY in session_state:
            quiz_state = session_state.pop(QUIZ_SESSION_STATE_KEY)
        self.quiz_skill.load_state(quiz_state)
        # тут возможна загрузка других ключей при необходимости

    def is_agree(self) -> bool:
        """Функция состояния.

        Проверяет, ответил ли пользователь согласием.

        Returns:
          True, если пользователь согласился.
        """
        return self.command == ServiceCommands.AGREE

    def is_disagree(self):
        """Функция состояния.

        Проверяет, ответил ли пользователем отказом.

        Returns:
          True, если пользователь отказался.
        """
        return self.command == ServiceCommands.DISAGREE
