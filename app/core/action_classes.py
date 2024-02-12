from transitions import MachineError

from app.constants.answers import Answers
from app.core.logger_initialize import logger
from app.machine import FiniteStateMachine


class BaseAction:
    """Базовый класс для основного класса действий."""

    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
    ) -> None:
        raise NotImplementedError


class Action(BaseAction):
    """Класса действий, запускает триггер."""

    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        trigger_name: str | None = None,
        command: str | None = None,
    ) -> str:
        """Функция запускающая триггер.

        Args:
            skill_obj: Объект класса `Skill`.
            trigger_name: Название триггера.
            command: Команда пользователя.

        Returns:
            Сообщение для пользователя.

        Raises:
            MachineError, если триггер вызван из не дозволенного состояния.
        """
        if trigger_name is None:
            return Answers.HELP_MAIN
        try:
            skill_obj.trigger(trigger_name)
        except MachineError:
            logger.debug(f"Команда вызвана из состояния {skill_obj.state}")
            skill_obj.message = "Отсюда нельзя вызвать эту команду"
        return skill_obj.message
