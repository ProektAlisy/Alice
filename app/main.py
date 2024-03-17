"""
Точка входа в приложение.
"""

import os

import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI

from app.constants.comands_states_answers import ERROR_MESSAGE
from app.core.exceptions import APIError
from app.core.logger_initialize import logger
from app.core.utils import check_api, get_error_response
from app.schemas import RequestData, ResponseData
from app.skill import get_skill_response

load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

application = FastAPI()


@application.post(
    "/",
    tags=["Alice project"],
    summary="Диалог с Алисой.",
)
async def root(data: RequestData) -> ResponseData:
    request_data = data.model_dump()
    try:
        check_api(data)
    except APIError:
        logger.error("Invalid request format!")
        return get_error_response(
            "Технические проблемы на стороне Яндекса. Попробуйте позже.",
        )
    try:
        result = get_skill_response(data)
    except Exception as e:
        logger.exception(e, exc_info=True)
        result = get_error_response(ERROR_MESSAGE)
    logger.info(
        "HISTORY",
        extra={
            "request": request_data,
            "response": result,
        },
    )
    return result
