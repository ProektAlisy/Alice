from fastapi import FastAPI
from icecream import ic
from pydantic import BaseModel
from transitions import MachineError

from app.machine import Skills


class RequestData(BaseModel):
    request: dict


app = FastAPI()

skill = Skills("Собака-поводырь")


class Command:
    def execute(self, skill: Skills) -> str:
        raise NotImplementedError


class InfoCenterCommand(Command):
    def execute(self, skill: Skills) -> str:
        try:
            skill.say_info_about_center()
        except MachineError:
            ic("Отсюда нельзя вызвать эту команду")
            skill.data["message"] = "Отсюда нельзя вызвать эту команду"
        return skill.data["message"]


class InfoPersonalCommand(Command):
    def execute(self, skill: Skills) -> str:
        skill.say_info_about_center_personal()
        return skill.data["message"]


class AdditionalInfo(Command):
    def execute(self, skill: Skills) -> str:
        if skill.state == "info_center":
            skill.say_info()
            return skill.data["message"]
        return "Эта команда доступна только в состоянии info_center"


class HelpCommand(Command):

    def execute(self, skill: Skills) -> str:
        skill.say_help()
        return skill.data["message"]


class HelpPhraseCommand(Command):
    def execute(self, skill: Skills) -> str:
        skill.say_help_phrase()
        return skill.data["message"]


class HelpNavigationCommand(Command):
    def execute(self, skill: Skills) -> str:
        skill.say_help_navigation()
        return skill.data["message"]


class HelpExitCommand(Command):

    def execute(self, skill: Skills) -> str:
        skill.from_help()
        return skill.data["message"]


command_mapping = {
    "расскажи о центре": InfoCenterCommand,
    "расскажи о персонале": InfoPersonalCommand,
    "дополнительная информация": AdditionalInfo,
    "помощь": HelpCommand,
    "хочу узнать фразы": HelpPhraseCommand,
    "помоги с навигацией": HelpNavigationCommand,
    "выход": HelpExitCommand,
}


@app.post("/")
async def root(data: RequestData):
    command = data.request.get("command")
    command_class = command_mapping.get(command.lower())

    if command_class:
        command_instance = command_class()
        answer = command_instance.execute(skill)
    elif command.lower() == "":
        answer = "Приветствую!"
    else:
        answer = "Я не понимаю, что вы хотите сказать"
    ic(command, skill.state)
    response = {
        "response": {
            "text": answer,
            "end_session": False,
        },
        "version": "1.0",
    }
    return response
