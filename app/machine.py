import logging

from transitions import Machine

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
)
from app.constants.commands import ServiceCommands
from app.constants.skill_transitions import TRANSITIONS
from app.constants.states import HELP_STATES, STATES
from app.quiz import QuizSkill
from app.utils import (
    create_trigger,
    get_after_answer_by_trigger,
    get_func_answers_command,
    get_trigger_by_command,
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
        self.progress = None
        self.incorrect_answers = 0
        self.command = ""
        self.machine = Machine(
            model=self,
            states=STATES + HELP_STATES,
            transitions=TRANSITIONS,
            initial="start",
        )
        self.flag = False
        self.max_progress = len(self.machine.states)
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
        if self.progress is None:
            self.progress = []
        if self.flag and current_step in [
            create_trigger(state) for state in STATES
        ]:
            self.progress = list(set(self.progress) - {current_step}) + [
                current_step,
            ]

    def _generate_function(self, name, message, command):
        """Генератор функций.

        Создаем сразу все функции, которые указаны в transitions класса
        FiniteStateMachine.
        Args:
            self: Объект FiniteStateMachine.
            name: Имя функции.
            message: Сообщение, которое зачитывает Алиса.
            command: Команда пользователя.
        """

        def _func():
            self.message = message
            self.incorrect_answers = 0
            self._save_progress(
                get_trigger_by_command(
                    command,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                ),
            )

        setattr(self, name, _func)

    def _create_agree_functions(self):
        [
            self._generate_function(
                func_name,
                answer + " " + after_answer,
                command,
            )
            for func_name, answer, after_answer, _, command in get_func_answers_command(  # noqa
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        ]

    def _create_disagree_functions(self) -> None:
        """Создание функций, обрабатывающих отказы пользователя.

        Args:
            self: Объект FiniteStateMachine.
        """
        [
            self._generate_function(
                func_name + "_disagree",
                disagree_answer,
                command,
            )
            for func_name, _, _, disagree_answer, command in get_func_answers_command(  # noqa
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        ]

    def get_next_after_answer(self, step: str) -> str:
        """Возвращает следующий ответ с вариантами действия пользователя.

        Args:
            step: Список пройденных состояний.

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        remaining_progress = self.get_remaining_answer(self.progress)
        try:
            index = remaining_progress.index(step)
        except ValueError:
            raise ValueError(
                f"Step {step} not found in progress {self.progress}",
            )
        try:
            next_trigger = remaining_progress[index + 1]
            get_after_answer_by_trigger(next_trigger)
        except IndexError:
            return "Вы закончили. Заглушка."

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
            dict(): словарь сохраненного состояния вида::

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

    def get_remaining_answer(self, progress: list[str]) -> list[str]:
        return [step for step in progress if step not in self.machine.states]
