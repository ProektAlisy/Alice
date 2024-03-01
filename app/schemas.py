from typing import Optional

from pydantic import BaseModel


class RequestData(BaseModel):
    session: dict
    request: dict
    state: Optional[dict]


class InnerResponse(BaseModel):
    text: str
    end_session: bool
    directives: dict | None


class ResponseData(BaseModel):
    response: InnerResponse
    session_state: dict
    version: str
