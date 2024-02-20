"""
Содержит класс с основным методом, запускающим все триггеры и классы,
соответствующие определенным условиям.
"""

from pprint import pprint

from icecream import ic

from app.constants.comands_triggers_answers import (
    COMMANDS_STATES_GET_FUNC_ANSWERS,
    ORDERED_STATES,
    another_answers_documents,
)
from app.constants.commands import Commands, ServiceCommands
from app.constants.intents import (
    ServiceIntents,
    INTENTS,
)
from app.constants.quiz.intents import QuizIntents
from app.constants.states import (
    MANUAL_TRAINING_STATE,
    QUIZ_TRIGGER_STATE,
)
from app.core.utils import (
    get_after_answer_by_trigger,
    get_all_commands,
    get_last_in_history,
    get_trigger_by_command,
    is_alice_commands,
    last_trigger,
    next_trigger,
    compose_message,
)
from app.machine import FiniteStateMachine

skill = FiniteStateMachine()
all_commands = get_all_commands(COMMANDS_STATES_GET_FUNC_ANSWERS)


class Command:
    """Базовый класс.

    Запускает определенное действие по определенному условию.
    """

    def __init__(self, skill_obj, command_instance):
        self.skill = skill_obj
        self.command_instance = command_instance

    def condition(
        self,
        intents: dict[str],
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
        intents: dict[str],
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
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> bool:
        """Определяем, не вызывается ли викторина."""
        return QuizIntents.TAKE_QUIZ in intents

    def execute(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> dict[str, str]:
        """Запуск викторины."""
        return skill.get_output(
            self.skill.quiz_skill.execute_command(command, intents)[1]
        )


class QuizSetState(Command):
    """Работа викторины."""

    @staticmethod
    def _get_quiz_after_agree_command():
        if skill.quiz_skill.is_finished() and skill.is_agree():
            after_answer = get_after_answer_by_trigger(
                QUIZ_TRIGGER_STATE,
                COMMANDS_STATES_GET_FUNC_ANSWERS,
            )
        elif skill.quiz_skill.is_finished():
            after_answer = skill.get_next_after_answer(QUIZ_TRIGGER_STATE)
        else:
            after_answer = ""
        return after_answer

    def condition(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> bool:
        """Проверяем, не окончена ли викторина."""
        return not skill.quiz_skill.is_finished()

    def execute(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> dict[str, str]:
        """Отвечаем на вопросы викторины."""
        self.skill.is_to_progress = True
        skill.save_progress(QUIZ_TRIGGER_STATE)
        skill.save_history(QUIZ_TRIGGER_STATE)
        result, answer = skill.quiz_skill.execute_command(command, intents)
        after_answer = self._get_quiz_after_agree_command()
        if result:
            return skill.get_output(compose_message(answer, after_answer))
        return skill.get_output(answer)


class ManualTrainingCommand(Command):
    """Фиксируем вызов обучения по методичке."""

    def condition(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> bool:
        """Определяем, нет ли команды вызова обучения по методичке."""
        return (
            INTENTS.TAKE_MANUAL_TRAINING in intents
            or command.lower() == Commands.TAKE_MANUAL_TRAINING
        )

    def execute(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> dict[str, str]:
        """Запуск обучения по методичке."""
        result, directives = skill.manual_training.process_request(
            command,
            intents,
        )
        return skill.get_output(
            result,
            directives=directives,
        )


class ManualTrainingSetState(Command):
    """Обучение по методичке в процессе."""

    @staticmethod
    def _get_manual_after_agree_command() -> str:
        """Возвращает вспомогательный ответ.

        После согласия (is_agree=True) пользователя на шаге обучения по
        методичке (state=MANUAL_TRAINING_TRIGGER_STATE).
        """
        if skill.manual_training.is_finished() and skill.is_agree():
            after_answer = get_after_answer_by_trigger(
                MANUAL_TRAINING_STATE,
                COMMANDS_STATES_GET_FUNC_ANSWERS,
            )
        elif skill.manual_training.is_finished():
            after_answer = skill.get_next_after_answer(MANUAL_TRAINING_STATE)
        else:
            after_answer = ""
        return after_answer

    def condition(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> bool:
        """Проверяем, не окончено ли обучение."""
        return not skill.manual_training.is_finish

    def execute(
        self,
        intents: dict[str],
        command: str,
        is_new: bool,
    ) -> dict[str, str]:
        """Проходим обучение по методичке."""
        self.skill.is_to_progress = True
        skill.save_progress(MANUAL_TRAINING_STATE)
        skill.save_history(MANUAL_TRAINING_STATE)
        answer, directives = skill.manual_training.process_request(
            command,
            intents,
        )
        after_answer = self._get_manual_after_agree_command()
        return skill.get_output(answer + after_answer, directives=directives)


class GreetingsCommand(Command):
    """Работа с приветствием."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие, для выполнения `execute`."""
        return not command and is_new

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Выводит приветствие."""
        return skill.get_output(
            another_answers_documents.get("full_greetings", "")
        )


class RepeatCommand(Command):
    """Работа с повторением сообщения."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие для выполнения `execute`."""
        return (
            command.lower() == ServiceCommands.REPEAT
            or ServiceIntents.REPEAT in intents
        )

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Вызываем последний триггер в истории состояний."""
        return self.command_instance.execute(
            self.skill,
            last_trigger(self.skill.history),
        )


class AliceCommandsCommand(Command):
    """Работа с командами Алисы."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Проверка, является ли команда командой Алисы."""
        return is_alice_commands(command)

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Вывод соответствующего ответа."""
        return skill.get_output(
            another_answers_documents.get("standard_alice_command", "")
        )


class AllCommandsCommand(Command):
    """Работа со всеми прямыми командами."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие для запуска `execute`."""
        return command.lower() in all_commands or INTENTS.get_available(
            intents,
        )

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Получение соответствующего ответа."""
        self.skill.is_to_progress = True
        greeting = (
            another_answers_documents.get("small_greetings", "")
            if is_new
            else ""
        )
        result = self.command_instance.execute(
            self.skill,
            get_trigger_by_command(
                command,
                intents,
                COMMANDS_STATES_GET_FUNC_ANSWERS,
            ),
        )
        return skill.get_output(f"{greeting} {result['response'].get('text')}")


class AgreeCommand(Command):
    """Обработка согласия пользователя."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return (
            command == ServiceCommands.AGREE or ServiceIntents.AGREE in intents
        )

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Получение соответствующего сообщения."""
        self.skill.is_to_progress = True
        trigger = self.skill.next_trigger_by_history(
            COMMANDS_STATES_GET_FUNC_ANSWERS,
        )
        if trigger == QUIZ_TRIGGER_STATE:
            answer = self.skill.quiz_skill.execute_command(
                "запусти викторину",
                QuizIntents.TAKE_QUIZ,
            )[1]
            return skill.get_output(answer)
        if trigger == MANUAL_TRAINING_STATE:
            self.skill.manual_training.is_finish = False
            answer, _ = self.skill.manual_training.process_request(
                "пройти обучение по методичке",
                INTENTS.TAKE_MANUAL_TRAINING,
            )
            return skill.get_output(answer)

        return self.command_instance.execute(
            self.skill,
            trigger,
        )


class DisagreeCommand(Command):
    """Работа с отказами пользователя."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return (
            command == ServiceCommands.DISAGREE
            or ServiceIntents.DISAGREE in intents
        )

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Получение соответствующего ответа для пользователя."""
        self.skill.is_to_progress = False
        return self.command_instance.execute(
            self.skill,
            next_trigger(
                get_last_in_history(self.skill.history),
                ORDERED_STATES,
            ),
        )


class ExitCommand(Command):
    """Обработка выхода из навыка."""

    def condition(self, intents: dict[str], command: str, is_new: bool):
        """Условие запуска `execute`."""
        return command == ServiceCommands.EXIT

    def execute(self, intents: dict[str], command: str, is_new: bool):
        """Обнуление прогресса и соответствующее сообщение пользователю."""
        self.skill.is_to_progress = False
        self.skill.history = []
        self.skill.progress = []
        return skill.get_output(
            another_answers_documents.get("exit_from_skill", ""),
            end_session=True,
        )
