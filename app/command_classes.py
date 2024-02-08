from icecream import ic
from transitions import MachineError

from app.constants.answers import Answers
from app.constants.comands_triggers_answers import (
    COMMANDS_TRIGGERS_GET_FUNC_ANSWERS,
    ORDERED_TRIGGERS,
    after_answers_documents,
)
from app.constants.commands import ServiceCommands
from app.constants.quiz.intents import Intents
from app.logger_initialize import logger
from app.machine import FiniteStateMachine
from app.utils import (
    get_all_commands,
    get_last_in_history,
    get_trigger_by_command,
    is_alice_commands,
    last_trigger,
    next_trigger,
)

skill = FiniteStateMachine()
all_commands = get_all_commands(COMMANDS_TRIGGERS_GET_FUNC_ANSWERS)


class BaseAction:
    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> None:
        raise NotImplementedError


class Action(BaseAction):
    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
        command: str | None = None,
    ) -> str:
        if trigger_name is None:
            return Answers.HELP_MAIN
        try:
            ic(trigger_name)
            skill_obj.trigger(trigger_name)
        except MachineError:
            logger.debug(f"Команда вызвана из состояния {skill_obj.state}")
            skill_obj.message = "Отсюда нельзя вызвать эту команду"
        return skill_obj.message


class Command:
    def __init__(self, skill_obj, command_instance):
        self.skill = skill_obj
        self.command_instance = command_instance

    def condition(self, intents, command, is_new):
        raise NotImplementedError

    def execute(self, intents, command, is_new):
        raise NotImplementedError


class QuizCommand(Command):
    def condition(self, intents, command, is_new):
        return (
            Intents.TAKE_QUIZ in intents
            or self.skill.progress
            and self.skill.progress[-1] == "trigger_take_quiz"
        )

    def execute(self, intents, command, is_new):
        self.skill.machine.set_state("take_quiz")
        return self.skill.quiz_skill.execute_command(command, intents)[1]


class QuizSetState(Command):
    def condition(self, intents, command, is_new):
        return skill.state == "take_quiz"

    def execute(self, intents, command, is_new):
        result, answer = skill.quiz_skill.execute_command(command, intents)
        after_quiz_message = ""
        if skill.quiz_skill.is_finished():
            # или надо сделать state = "after_quiz" c выбором след. пункта
            skill.state = "start"
            self.skill.is_to_progress = True
            after_quiz_message = (
                self.command_instance.execute(
                    self.skill,
                    None,
                    # self.skill.next_trigger_by_progress(
                    #     COMMANDS_TRIGGERS_GET_FUNC_ANSWERS
                    # ),
                )
                + "Продолжим?"
            )
        if result:
            return answer + after_quiz_message


class GreetingsCommand(Command):
    def condition(self, intents, command, is_new):
        return not command and is_new

    def execute(self, intents, command, is_new):
        return Answers.FULL_GREETINGS


class RepeatCommand(Command):
    def condition(self, intents, command, is_new):
        return command.lower() == ServiceCommands.REPEAT

    def execute(self, intents, command, is_new):
        return self.command_instance.execute(
            self.skill, last_trigger(self.skill.history)
        )


class AliceCommandsCommand(Command):
    def condition(self, intents, command, is_new):
        return is_alice_commands(command)

    def execute(self, intents, command, is_new):
        return Answers.STANDARD_ALICE_COMMAND


class AllCommandsCommand(Command):
    def condition(self, intents, command, is_new):
        return command.lower() in all_commands

    def execute(self, intents, command, is_new):
        self.skill.is_to_progress = True
        return (
            Answers.SMALL_GREETINGS if is_new else ""
        ) + self.command_instance.execute(
            self.skill,
            get_trigger_by_command(
                command, COMMANDS_TRIGGERS_GET_FUNC_ANSWERS
            ),
        )


class AgreeCommand(Command):
    def condition(self, intents, command, is_new):
        return command == ServiceCommands.AGREE

    def execute(self, intents, command, is_new):
        self.skill.is_to_progress = True
        return self.command_instance.execute(
            self.skill,
            self.skill.next_trigger_by_progress(
                COMMANDS_TRIGGERS_GET_FUNC_ANSWERS
            ),
        )


class DisagreeCommand(Command):
    def condition(self, intents, command, is_new):
        return command == ServiceCommands.DISAGREE

    def execute(self, intents, command, is_new):
        self.skill.is_to_progress = False
        return self.command_instance.execute(
            self.skill,
            next_trigger(
                get_last_in_history(self.skill.history), ORDERED_TRIGGERS
            ),
        )


class ExitCommand(Command):
    def condition(self, intents, command, is_new):
        return command == ServiceCommands.EXIT

    def execute(self, intents, command, is_new):
        self.skill.is_to_progress = False
        return Answers.EXIT_FROM_SKILL
