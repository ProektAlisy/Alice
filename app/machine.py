# from transitions import Machine
from icecream import ic

from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
    ORDERED_TRIGGERS,
    another_answers_documents,
)
from app.constants.commands import ServiceCommands
from app.constants.states import (
    CORE_TRIGGERS,
    HELP_STATES,
    STATES,
    TRIGGER_HELP_MAIN,
    TRIGGERS_BY_GROUP,
)
from app.core.utils import (
    create_trigger,
    disagree_answer_by_trigger,
    find_previous_element,
    get_after_answer_by_trigger,
    get_answer_by_trigger,
    get_disagree_answer_by_trigger,
    get_triggers_by_order,
    get_triggers_group_by_trigger,
    last_trigger,
    next_trigger,
)
from app.guidebook_player import AudioAssistant
from app.quiz.quizskill import QuizSkill

QUIZ_SESSION_STATE_KEY = "quiz_state"


class FiniteStateMachine:
    """Класс навыка.

    Определяет правила перехода между состояниями навыка.

    Attributes:
        message(str): Сообщение, которое зачитывает Алиса.
        progress(list[str]): Прогресс прохождения всех историй в навыке.
        incorrect_answers(int): Количество неправильных ответов.
        command(str): Команда пользователя (в дальнейшем заменим на интенты).
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
        self.manual_training = AudioAssistant()

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

    def action_func(self, trigger_name: str) -> callable:
        """Флаг согласия/отказа.

        Args:
            trigger_name:
            self: Объект FiniteStateMachine.
        """

        if self.is_disagree():
            self.disagree_function(trigger_name)
        else:
            self.agree_function(trigger_name)

    def save_progress(self, current_step: str) -> None:
        """Прогресс прохождения навыка.

        Сохраняет состояние прохождения навыка.

        Args:
            self: Объект FiniteStateMachine.
            current_step: Состояние навыка.
        """
        if self.is_to_progress and current_step in [
            create_trigger(state) for state in STATES[1:]
        ]:
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
            current_step: Текущее состояние (соответствующий триггер).
        """
        self.history = list(set(self.progress) - {current_step}) + [
            current_step,
        ]

    def agree_function(self, trigger):
        """Создает функции, вызываемые триггерами.

        Создаем сразу все функции, которые указаны в transitions класса
        FiniteStateMachine.
        Args:
            trigger: Вызванная триггер.
        """
        self.save_progress(trigger)
        self.save_history(trigger)
        answer = self._get_answer(trigger)
        after_answer = self._get_after_answer(trigger)
        self.message = self._compose_message(answer, after_answer)
        self.incorrect_answers = 0

    def disagree_function(self, trigger: str) -> None:
        """Создает `disagree_` функцию.
        Вызывается триггером, соответствующим отказу пользователя.

        Args:
            trigger: Триггер, по которому вызываем функцию.
        """
        ic(trigger, "disagree")
        self.save_progress(trigger)
        if trigger in CORE_TRIGGERS:
            self.history.extend(
                get_triggers_group_by_trigger(
                    trigger,
                    TRIGGERS_BY_GROUP,
                ),
            )
        else:
            self.save_history(trigger)
        disagree_answer = self.get_next_disagree_answer(
            trigger,
        )
        self.message = disagree_answer
        self.incorrect_answers = 0

    def _get_answer(self, trigger: str) -> str:
        """Генерирует основной ответ навыка по триггеру.

        Args:
            trigger: Триггер, по которому генерируем ответ.

        Returns:
            Ответ навыка.
        """
        if self._is_repeat_and_previous_disagree():
            return disagree_answer_by_trigger(
                trigger,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        return get_answer_by_trigger(
            trigger,
            COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
        )

    def _get_after_answer(self, trigger: str) -> str:
        """Генерирует вторую часть ответа с подсказкой о продолжении.

        Args:
            trigger: Триггер, по которому генерируем подсказку.

        Returns:
            Подсказка.
        """
        if self.is_agree() and not self._is_repeat_and_previous_disagree():
            return get_after_answer_by_trigger(
                trigger,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        if not self._is_repeat_and_previous_disagree():
            return self.get_next_after_answer(trigger)
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

    @staticmethod
    def _compose_message(answer: str, after_answer: str) -> str:
        """Составляем сообщение пользователю.

        Args:
            answer: Основная часть ответа.
            after_answer: Часть ответа с подсказкой о продолжении.

        Returns:
            Полный ответ.
        """
        return f"{answer} {after_answer}"

    def get_next_after_answer(self, step: str) -> str:
        """Возвращает следующий ответ с подсказкой для пользователя.

        Args:
            step: Текущее состояние (соответствующий триггер).

        Returns:
            Добавленный ответ к основному, содержит варианты действия
            пользователя.
        """
        while step in self.progress:
            step = self.next_trigger_by_history(
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            )
        # исправляем border effect, когда в помощи появляется `after_answer`
        if step == TRIGGER_HELP_MAIN:
            return ""
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
            self.history[-1],
            COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
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

    def next_trigger_by_history(
        self,
        triggers: list,
    ) -> str:
        """Возвращает следующий триггер.

        Очередность определяется списком состояний STATES в states.py.
        Учитывается прогресс пользователя.

        Args:
            triggers: Список всех триггеров.

        Returns:
            Триггер, соответствующий первой непройденной истории/возможности
            после последнего выполненного действия.
        """
        trigger = last_trigger(self.history)
        ordered_triggers = get_triggers_by_order(triggers)
        if trigger is None:
            return ordered_triggers[0]
        trigger_index = ordered_triggers.index(trigger)
        len_triggers = len(ordered_triggers)
        for index in range(trigger_index, len_triggers + trigger_index):
            if ordered_triggers[index % len_triggers] in self.history:
                continue
            return ordered_triggers[index % len_triggers]

    def get_output(
        self,
        answer_text,
        directives=None,
        end_session=False,
    ) -> dict[str, str]:
        """Функция возвращает словарь с ответом и дополнительными данными."""
        return {
            "response": {
                "text": answer_text,
                "end_session": end_session,
                "directives": directives,
            },
            "session_state": self.dump_session_state(),
            "version": "1.0",
        }
