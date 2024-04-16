"""
Загружаем ответы пользователю из папки app/constants/
"""

from pathlib import Path

from app.core.logger_initialize import logger
from app.core.utils import read_from_files

constants_path = Path(__file__).resolve().parent.parent / "constants"

answers_documents = read_from_files(constants_path / "answers")
after_answers_documents = read_from_files(constants_path / "after_answers")
disagree_answers_documents = read_from_files(
    constants_path / "disagree_answers"
)
another_answers_documents = read_from_files(constants_path / "another_answers")

logger.info("Загрузка ответов завершена.")
