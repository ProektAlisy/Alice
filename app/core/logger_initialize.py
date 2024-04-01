import logging
import os
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

from app.settings import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record,
            record,
            message_dict,
        )
        if not log_record.get("timestamp"):
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s",
    json_ensure_ascii=False,
)

os.makedirs(settings.LOG_DIR, exist_ok=True)
logger = logging.getLogger()
log_handler = RotatingFileHandler(
    filename=os.path.join(settings.LOG_DIR, settings.LOG_FILE),
    maxBytes=settings.LOG_FILE_SIZE,
    backupCount=settings.LOG_FILES_COUNT,
    encoding="utf-8",
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(settings.LOG_LEVEL)
