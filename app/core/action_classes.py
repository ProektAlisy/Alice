from app.constants.comands_states_answers import another_answers_documents
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
    """Класс действия."""

    @staticmethod
    def execute(
        skill_obj: FiniteStateMachine,
        state_name: str | None = None,
        command: str | None = None,
    ) -> dict[str, str]:
        """Функция выполняющая переход в заданное состояние.

        Args:
            skill_obj: Объект класса `Skill`.
            state_name: Название состояния.
            command: Команда пользователя.

        Returns:
            Сообщение для пользователя.
        """
        if state_name is None:
            return skill_obj.get_output(
                another_answers_documents.get(
                    "full_greetings",
                    "",
                ),
            )
        skill_obj.action_func(state_name)
        return skill_obj.get_output(skill_obj.message)
