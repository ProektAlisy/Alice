from typing import Optional

from pydantic import BaseModel


class RequestData(BaseModel):
    session: dict
    request: dict
    state: Optional[dict]

    def is_audio_player_type(self) -> bool:
        return self.request["type"].startswith("AudioPlayer")

    def is_simple_utterance_type(self) -> bool:
        return self.request["type"] == "SimpleUtterance"


class InnerResponse(BaseModel):
    text: str
    end_session: bool
    directives: dict | None


class ResponseData(BaseModel):
    response: InnerResponse
    session_state: dict
    version: str
