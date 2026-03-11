import json
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import log

logger = logging.getLogger("reports")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_weekday(date: str) -> int:
    """функция, получающая день недели в цифрах"""
    logger.info(f"start get_date {date}")
    date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    weekday = date_obj.isocalendar()
    result = weekday[2]
    logger.info(f"the resulting list {result}")
    return result


@log()
def spending_by_weekday(operations: pd.DataFrame, date: Optional[str] = None) -> str:
    """функция, возращающая датафрейм в виде средних трат по дням недели"""
    logger.info(f"start spending_by_weekday {operations}, {date}")
    if date is None:
        date_ = datetime.now()
    else:
        date_ = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
    transactions = operations.to_dict(orient="records")
    sorted_by_date_list = []
    monday, tuesday, wednesday, thursday, friday, saturday, sunday = [], [], [], [], [], [], []

    weekdays = {"Понедельник": 0, "Вторник": 0, "Среда": 0, "Четверг": 0, "Пятница": 0, "Суббота": 0, "Воскресенье": 0}
    old_date = date_ - relativedelta(months=3)

    for element in transactions:
        if element["Дата операции"] and element["Сумма операции"] < 0:
            if old_date <= datetime.strptime((element["Дата операции"]), "%d.%m.%Y %H:%M:%S") <= date_:
                sorted_by_date_list.append(element)

    for element in sorted_by_date_list:
        if get_weekday(str(element["Дата операции"])) == 1:
            monday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 2:
            tuesday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 3:
            wednesday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 4:
            thursday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 5:
            friday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 6:
            saturday.append(element["Сумма платежа"] * -1)
        elif get_weekday(str(element["Дата операции"])) == 7:
            sunday.append(element["Сумма платежа"] * -1)
        else:
            continue

    if len(monday) <= 0:
        weekdays["Понедельник"] = sum(monday) / 1
    else:
        weekdays["Понедельник"] = sum(monday) / len(monday)
    if len(tuesday) <= 0:
        weekdays["Вторник"] = sum(tuesday) / 1
    else:
        weekdays["Вторник"] = sum(tuesday) / len(tuesday)
    if len(wednesday) <= 0:
        weekdays["Среда"] = sum(wednesday) / 1
    else:
        weekdays["Среда"] = sum(wednesday) / len(wednesday)
    if len(thursday) <= 0:
        weekdays["Четверг"] = sum(thursday) / 1
    else:
        weekdays["Четверг"] = sum(thursday) / len(thursday)
    if len(friday) <= 0:
        weekdays["Пятница"] = sum(friday) / 1
    else:
        weekdays["Пятница"] = sum(friday) / len(friday)
    if len(saturday) <= 0:
        weekdays["Суббота"] = sum(saturday) / 1
    else:
        weekdays["Суббота"] = sum(saturday) / len(saturday)
    if len(sunday) <= 0:
        weekdays["Воскресенье"] = sum(sunday) / 1
    else:
        weekdays["Воскресенье"] = sum(sunday) / len(sunday)

    result = json.dumps(weekdays, ensure_ascii=False)
    logger.info(f"the resulting list {result}")

    print(result)
    return result
