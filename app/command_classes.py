import logging

from transitions import MachineError

from app.constants.answers import Answers
from app.constants.commands_triggers_functions import Commands, Triggers
from app.machine import FiniteStateMachine

skill = FiniteStateMachine()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s, %(levelname)s, %(message)s",
)
logger = logging.getLogger(__name__)


class Command:
    """
    A static method to execute the given skill on the specified target state.
    """
    @staticmethod
    def execute(
        skill: FiniteStateMachine, target_state: str | None = None
    ) -> str:
        raise NotImplementedError


class NextCommand(Command):
    """
    Executes the given skill by triggering the specified trigger_name,
    if provided.
    """
    @staticmethod
    def execute(
        skill: FiniteStateMachine, trigger_name: str | None = None
    ) -> str:
        try:
            skill.trigger(trigger_name)
        except MachineError:
            logger.debug(
                f"Команда вызвана из состояния {skill.state}, "
                f"а не из start"
            )
            skill.message = "Отсюда нельзя вызвать эту команду"
        return skill.message


def create_command_class(name: str, trigger_name: str, message: str):
    """
    Create a command class with the given name, trigger_name, and message.
    The execute method triggers the specified skill, sets the message,
    and handles MachineError exceptions. Returns the skill message.
    """
    class CustomCommand(Command):
        def execute(
            self, skill: FiniteStateMachine, target_state: str | None = None
        ) -> str:
            try:
                skill.trigger(trigger_name)
                skill.message = message
            except MachineError:
                logger.debug(
                    f"Команда вызвана из состояния {skill.state}, "
                    "а не из start"
                )
                skill.message = "Отсюда нельзя вызвать эту команду"
            return skill.message

    CustomCommand.__name__ = name
    return CustomCommand


commands = {
    Commands.NEXT: create_command_class(
        "NextCommand",
        "trigger",
        Answers.ABOUT_TRAINING_CENTER,
    ),
    Commands.ABOUT_TRAINING_CENTER: create_command_class(
        "TrainingCenterCommand",
        Triggers.ABOUT_TRAINING_CENTER,
        Answers.ABOUT_TRAINING_CENTER,
    ),
    Commands.ABOUT_STAFF: create_command_class(
        "StaffCommand",
        Triggers.ABOUT_STAFF,
        Answers.ABOUT_STAFF,
    ),
    Commands.ABOUT_ACCOMMODATION: create_command_class(
        "AccommodationCommand",
        Triggers.ABOUT_ACCOMMODATION,
        Answers.ABOUT_ACCOMMODATION,
    ),
    Commands.ABOUT_FACILITY: create_command_class(
        "FacilityCommand",
        Triggers.ABOUT_FACILITY,
        Answers.ABOUT_FACILITY,
    ),
    Commands.TAKE_TRAINING: create_command_class(
        "TakeTrainingCommand",
        Triggers.TAKE_TRAINING,
        Answers.TAKE_TRAINING,
    ),
    Commands.TAKE_QUIZ: create_command_class(
        "TakeQuizCommand",
        Triggers.TAKE_QUIZ,
        Answers.TAKE_QUIZ,
    ),
    Commands.LISTEN_TO_LEGISLATION: create_command_class(
        "TakeLegislationCommand",
        Triggers.LISTEN_TO_LEGISLATION,
        Answers.LISTEN_TO_LEGISLATION,
    ),
    Commands.ABOUT_ACCESSIBILITY: create_command_class(
        "AccessibilityCommand",
        Triggers.ABOUT_ACCESSIBILITY,
        Answers.ABOUT_ACCESSIBILITY,
    ),
    Commands.ABOUT_GUIDE_DOG_TRANSPORTATION: create_command_class(
        "DogTransportationCommand",
        Triggers.ABOUT_GUIDE_DOG_TRANSPORTATION,
        Answers.ABOUT_GUIDE_DOG_TRANSPORTATION,
    ),
    Commands.SELF_DEFENSE_PHRASE: create_command_class(
        "SelfDefenseCommand",
        Triggers.SELF_DEFENSE_PHRASE,
        Answers.SELF_DEFENSE_PHRASE,
    ),

    Commands.ABOUT_DISCOUNTS_AND_FREE_SERVICES: create_command_class(
        "DiscountsFreeServicesCommand",
        Triggers.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
        Answers.ABOUT_DISCOUNTS_AND_FREE_SERVICES,
    ),
    Commands.DISCOUNTS_FOR_FOOD: create_command_class(
        "DiscountsForFoodCommand",
        Triggers.DISCOUNTS_FOR_FOOD,
        Answers.DISCOUNTS_FOR_FOOD,
    ),
    Commands.DISCOUNTS_FOR_DELICACY: create_command_class(
        "DiscountsForDelicacyCommand",
        Triggers.DISCOUNTS_FOR_DELICACY,
        Answers.DISCOUNTS_FOR_DELICACY,
    ),
    Commands.SPECIAL_OFFERS_FOR_VETERINARIES: create_command_class(
        "DiscountsForVeterinariesCommand",
        Triggers.SPECIAL_OFFERS_FOR_VETERINARIES,
        Answers.SPECIAL_OFFERS_FOR_VETERINARIES,
    ),

    Commands.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS: create_command_class(
        "SupportServicesForBlindCommand",
        Triggers.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
        Answers.ABOUT_SUPPORT_SERVICES_FOR_BLIND_PASSENGERS,
    ),

    Commands.ABOUT_SERVICES_UNITING_BLIND_PEOPLE: create_command_class(
        "ServicesForBlindCommand",
        Triggers.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
        Answers.ABOUT_SERVICES_UNITING_BLIND_PEOPLE,
    ),
    Commands.ABOUT_REGIONAL_CLUBS: create_command_class(
        "RegionalClubsCommand",
        Triggers.ABOUT_REGIONAL_CLUBS,
        Answers.ABOUT_REGIONAL_CLUBS,
    ),
    Commands.ABOUT_SPECIAL_VIEW_FOUNDATION: create_command_class(
        "SpecialViewFoundationCommand",
        Triggers.ABOUT_SPECIAL_VIEW_FOUNDATION,
        Answers.ABOUT_SPECIAL_VIEW_FOUNDATION,
    ),

    Commands.INSTRUCTIONS_FOR_LAUNCHING_PODCAST: create_command_class(
        "InstructionsForLaunchingPodcastCommand",
        Triggers.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
        Answers.INSTRUCTIONS_FOR_LAUNCHING_PODCAST,
    ),

    Commands.HELP: create_command_class(
        "HelpCommand",
        Triggers.HELP,
        Answers.HELP_MAIN,
    ),
    Commands.HELP_PHRASE: create_command_class(
        "HelpPhraseCommand",
        Triggers.HELP_PHRASE,
        Answers.HELP_PHRASE,
    ),
    Commands.HELP_NAVIGATION: create_command_class(
        "HelpNavigationCommand",
        Triggers.HELP_NAVIGATION,
        Answers.HELP_NAVIGATION,
    ),
    Commands.HELP_EXIT: create_command_class(
        "HelpExit",
        Triggers.HELP_EXIT,
        Answers.EXIT_FROM_HELP,
    ),

    Commands.EXIT_FROM_LEGISLATION: create_command_class(
        "ExitLegislationCommand",
        Triggers.EXIT_FROM_LEGISLATION,
        Answers.EXIT_FROM_LEGISLATION,
    ),

    Commands.EXIT_DISCOUNTS_AND_FREE_SERVICES: create_command_class(
        "ExitDiscountsAndFreeServicesCommand",
        Triggers.EXIT_DISCOUNTS_AND_FREE_SERVICES,
        Answers.EXIT_DISCOUNTS_AND_FREE_SERVICES,
    ),

    Commands.EXIT_SERVICES_FOR_BLIND: create_command_class(
        "ExitCommand",
        Triggers.EXIT_SERVICES_FOR_BLIND,
        Answers.EXIT_SERVICES_FOR_BLIND,
    ),
}
