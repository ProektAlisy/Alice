from icecream import ic

from app.constants.comands_triggers_answers import another_answers_documents
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
    ) -> dict[str, str]:
        """Функция запускающая триггер.

        Args:
            skill_obj: Объект класса `Skill`.
            trigger_name: Название триггера.
            command: Команда пользователя.

        Returns:
            Сообщение для пользователя.
        """
        if trigger_name is None:
            return skill_obj.get_output(
                another_answers_documents.get("full_greetings", "")
            )
        skill_obj.action_func(trigger_name)
        return skill_obj.get_output(skill_obj.message)