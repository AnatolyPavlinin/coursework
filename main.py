import os.path

import pandas as pd

from src.reports import spending_by_weekday
from src.services import get_operations_dict
from src.views import get_json_answer, file_path

if __name__ == "__main__":

    """основная функция"""
    date = input("Введите пожалуйста время, по которому хотите запуск программы (формат YYYY.MM.DD HH:MM:SS)\n")
    print(get_json_answer(date))
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    transactions = get_operations_dict(file_path)

    user_input = input(
        "Хотите проанализировать ваши траты по дням недели за последние три месяца " "(от переданной даты)? Да/Нет\n"
    ).lower()
    if user_input == "да":
        new_date = input("Введите дату (формат 10.08.2020 15:20:10)\n").lower()
        print(spending_by_weekday(pd.DataFrame(transactions), new_date))
