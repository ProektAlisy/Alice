"""
Содержит класс с основным методом, запускающим все триггеры и классы,
соответствующие определенным условиям.
"""
from transitions import MachineError

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
    ORDERED_TRIGGERS,
    another_answers_documents,
)
from app.constants.commands import ServiceCommands
from app.constants.quiz.intents import ServiceIntents
from app.constants.quiz.intents import Intents
from app.constants.states import QUIZ_STATE, QUIZ_TRIGGER_STATE
from app.machine import FiniteStateMachine
from app.core.utils import (
    get_after_answer_by_trigger,
    get_all_commands,
    get_last_in_history,
    get_trigger_by_command,
    is_alice_commands,
    last_trigger,
    next_trigger,
)

skill = FiniteStateMachine()
all_commands = get_all_commands(COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)


class Command:
    """Базовый класс.

    Запускает определенное действие по определенному условию.
    """

    def __init__(self, skill_obj, command_instance):
        self.skill = skill_obj
        self.command_instance = command_instance

    def condition(
        self,
        intents: list[str],
        command: str,
        is_new: bool,
    ) -> None:
        """Определение условия при котором выполнится `execute`.

        Args:
            intents: Интенты для викторины.
            command: Команда пользователя.
            is_new: Это первое сообщение?

        Returns:
            True, если условие выполнено.
        """
        raise NotImplementedError

    def execute(
        self,
        intents: list[str],
        command: str,
        is_new: bool,
    ) -> None:
        """Определение условия действия, при котором выполнится `execute`.

        Args:
            intents: Интенты для викторины.
            command: Команда пользователя.
            is_new: Это первое сообщение?

        Returns:
            True, если условие выполнено.
        """
        raise NotImplementedError


class QuizCommand(Command):
    """Фиксируем вызов викторины."""

    def condition(
        self,
        intents: list[str],
        command: str,
        is_new: bool,
    ) -> bool:
        """Определяем, не вызывается ли викторина."""
        return Intents.TAKE_QUIZ in intents

    def execute(
        self,
        intents: list[str],
        command: str,
        is_new: bool,
    ) -> str:
        """Запуск викторины."""
        return self.skill.quiz_skill.execute_command(command, intents)[1]


class QuizSetState(Command):
    """Работа викторины."""

    def condition(
        self, intents: list[str], command: str, is_new: bool
    ) -> bool:
        """Проверяем, не окончена ли викторина."""
        return not skill.quiz_skill.is_finished()

    def execute(
        self,
        intents: list[str],
        command: str,
        is_new: bool,
    ) -> str:
        """Отвечаем на вопросы викторины."""
        self.skill.is_to_progress = True
        skill.save_progress(QUIZ_TRIGGER_STATE)
        skill.save_history(QUIZ_TRIGGER_STATE)
        result, answer = skill.quiz_skill.execute_command(command, intents)
        if skill.quiz_skill.is_finished():
            if skill.is_agree():
                after_answer = get_after_answer_by_trigger(
                    QUIZ_TRIGGER_STATE,
                    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
                )
            else:
                after_answer = skill.get_next_after_answer(QUIZ_TRIGGER_STATE)
        else:
            after_answer = ""

        if result:
            return answer + after_answer
        return answer


class GreetingsCommand(Command):
    """Работа с приветствием."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие, для выполнения `execute`."""
        return not command and is_new

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Выводит приветствие."""
        return another_answers_documents.get("full_greetings", [])


class RepeatCommand(Command):
    """Работа с повторением сообщения."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие для выполнения `execute`."""
        return command.lower() == ServiceCommands.REPEAT

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Вызываем последний триггер в истории состояний."""
        return self.command_instance.execute(
            self.skill,
            last_trigger(self.skill.history),
        )


class AliceCommandsCommand(Command):
    """Работа с командами Алисы."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Проверка, является ли команда командой Алисы."""
        return is_alice_commands(command)

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Вывод соответствующего ответа."""
        return another_answers_documents.get("standard_alice_command", [])


class AllCommandsCommand(Command):
    """Работа со всеми прямыми командами."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие для запуска `execute`."""
        return command.lower() in all_commands or Intents.get_available(
            intents
        )

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Получение соответствующего ответа."""
        self.skill.is_to_progress = True
        greeting = (
            another_answers_documents.get("small_greetings", [])
            if is_new
            else ""
        )
        answer = self.command_instance.execute(
            self.skill,
            get_trigger_by_command(
                command,
                intents,
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
            ),
        )
        return f"{greeting}. {answer}"


class AgreeCommand(Command):
    """Обработка согласия пользователя."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return (
            command == ServiceCommands.AGREE or ServiceIntents.AGREE in intents
        )

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Получение соответствующего сообщения."""
        self.skill.is_to_progress = True
        trigger = self.skill.next_trigger_by_history(
            COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
        )
        if trigger == QUIZ_TRIGGER_STATE:
            self.skill.machine.set_state(QUIZ_STATE)
            return self.skill.quiz_skill.execute_command(
                "запусти викторину",
                Intents.TAKE_QUIZ,
            )[1]
        return self.command_instance.execute(
            self.skill,
            trigger,
        )


class DisagreeCommand(Command):
    """Работа с отказами пользователя."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return (
            command == ServiceCommands.DISAGREE
            or ServiceIntents.DISAGREE in intents
        )

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Получение соответствующего ответа для пользователя."""
        self.skill.is_to_progress = False
        return self.command_instance.execute(
            self.skill,
            next_trigger(
                get_last_in_history(self.skill.history),
                ORDERED_TRIGGERS,
            ),
        )


class ExitCommand(Command):
    """Обработка выхода из навыка."""

    def condition(self, intents: list[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return command == ServiceCommands.EXIT

    def execute(self, intents: list[str], command: str, is_new: bool):
        """Обнуление прогресса и соответствующее сообщение пользователю."""
        self.skill.is_to_progress = False
        self.skill.history = []
        self.skill.progress = []
        return another_answers_documents.get("exit_from_skill", [])
