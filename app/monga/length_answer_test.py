from icecream import ic

from app.constants.comands_states_answers import (
    answers_documents,
    after_answers_documents,
)
from app.core.logger_initialize import logger

ic(answers_documents, after_answers_documents)
num_of_errors = 0
for answer in answers_documents.values():
    for after_answer in after_answers_documents.values():
        if len(after_answer) + len(answer) > 1024:
            num_of_errors += 1
            logger.info(f"{answer} \n {after_answer}")
logger.info(f"Число превышений 1024 символа: {num_of_errors}")
