import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from pythonjsonlogger import jsonlogger

LOG_FILENAME = "alice.log"

load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record,
            record,
            message_dict,
        )
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s",
    json_ensure_ascii=False,
)

logger = logging.getLogger()
log_handler = RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=10_000_000,
    backupCount=10,
    encoding="utf-8",
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
logger.setLevel(log_level)
