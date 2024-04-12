from typing import Optional

from pydantic import BaseModel


class AudioPlayerState(BaseModel):
    token: str
    offset_ms: int
    state: str


class RequestData(BaseModel):
    session: dict
    request: dict
    state: Optional[dict]

    def is_audio_player_type(self) -> bool:
        return self.request["type"].startswith("AudioPlayer")

    def is_simple_utterance_type(self) -> bool:
        return self.request["type"] == "SimpleUtterance"

    def get_audio_player_state(self) -> AudioPlayerState | None:
        audio_player = self.state.get("audio_player")
        if audio_player:
            return AudioPlayerState(**audio_player)
        return None


class InnerResponse(BaseModel):
    text: str
    end_session: bool
    should_listen: bool | None = None
    directives: dict | None


class ResponseData(BaseModel):
    response: InnerResponse
    session_state: dict
    version: str
