import json
import logging
from datetime import datetime

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def hi_message(date: str) -> str | None:
    """Функция, возращающая приветствие в зависимости от времени"""

    logger.info("Анализируем, какое приветствие выбрать")
    current_date = datetime.strptime(date, "%Y.%m.%d %H:%M:%S").time()

    if 5 <= current_date.hour < 12:
        greeting = "Доброе утро!"
    elif 12 <= current_date.hour < 17:
        greeting = "Добрый день!"
    elif 17 <= current_date.hour < 23:
        greeting = "Добрый вечер!"
    else:
        greeting = "Доброй ночи!"

    logger.info(f"Приветствие будет: {greeting}")

    return json.dumps(greeting, ensure_ascii=False, indent=4)
