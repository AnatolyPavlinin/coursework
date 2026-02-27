import json
import logging
import os
from heapq import nlargest
from pathlib import Path
from typing import Any, Dict, Sequence

import pandas as pd
import requests
from dotenv import load_dotenv

from src.services import get_operations_dict
from src.utils import hi_message

current_dir = Path(__file__).parent
project_root = current_dir.parent
file_path = project_root / "data" / "operations.xlsx"

load_dotenv()
API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")

logger = logging.getLogger("views")
file_handler = logging.FileHandler("loggers_info.txt")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_json_answer(date: str) -> Sequence[object] | str:
    """Функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающая JSON-ответ со следующими данными:
    1. Приветствие
    2. По каждой карте: последние 4 цифры карты; общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей).
    3. Топ-5 транзакций по сумме платежа.
    4. Курс валют.
    5. Стоимость акций из S&P500."""
    logger.info("start get_json_answer")
    card_numbers = []
    special_cards = []
    total_sum = []
    top_transactions = []
    stock_prices = []
    currency_rates = []
    currency = ["USD", "EUR"]
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    out_put_func: Dict[str, Any] = {
        "greeting": "",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [Sequence[str]],
        "stock_prices": [],
    }

    greeting = hi_message(date)

    out_put_func["greeting"] = greeting
    for item in currency:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY_1}/latest/{item}"
        response = requests.get(url, headers={"apikey": API_KEY_1})
        response_data = response.json()
        path = response_data.get("conversion_rates", {}).get("RUB")
        currency_rates.append(dict(currency=item, rate=path))
    out_put_func["currency_rates"] = currency_rates

    data = get_operations_dict(file_path)
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            card_numbers.append(dict(last_digits=transaction.get("Номер карты", "").replace("*", "")))
    for card in card_numbers:
        if card not in special_cards:
            special_cards.append(card)
    for transaction in data:
        if not pd.isnull(transaction.get("Номер карты")):
            for special in special_cards:
                if special.get("last_digits", "") in transaction.get("Номер карты", ""):
                    if pd.isnull(transaction.get("Сумма операции", "")) is False:
                        try:
                            special["total_spent"] += abs(transaction.get("Сумма операции", ""))
                            special["cashback"] += abs(transaction.get("Сумма операции", "") / 100)
                        except KeyError:
                            special["total_spent"] = transaction.get("Сумма операции", "")
                            special["cashback"] = abs(transaction.get("Сумма операции", "") / 100)
    for special in special_cards:
        special["total_spent"] = str(round(float(special.get("total_spent", "0")), 2))
        special["cashback"] = str(round(float(special.get("cashback", "0")), 2))
    out_put_func["cards"] = special_cards

    for transaction in data:
        total_sum.append(transaction.get("Сумма операции"))
    total_sum = nlargest(5, total_sum)
    for transaction in data:
        for amount in total_sum:
            if transaction.get("Сумма операции") == amount:
                top_transactions.append(
                    dict(
                        date=transaction.get("Дата платежа"),
                        amount=amount,
                        category=transaction.get("Категория"),
                        description=transaction.get("Описание"),
                    )
                )
                total_sum.remove(amount)
    out_put_func["top_transactions"] = top_transactions

    # url_2 = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={API_KEY_2}"
    url_2 = "https://financialmodelingprep.com/stable/search-exchange-variants?&apikey={API_KEY_2}"
    response_2 = requests.get(url_2)
    response_data_2 = response_2.json()

    print(f"Тип response_data_2: {type(response_data_2)}")
    print(f"Содержимое: {response_data_2}")

    for share in response_data_2:
        for stock in stocks:
            if share.get("symbol", "") == stock:
                stock_prices.append(dict(stock=stock, price=share.get("price", "")))
    out_put_func["stock_prices"] = stock_prices

    json_data = json.dumps(out_put_func, ensure_ascii=False, indent=4)
    logger.info(f"The end of get_json_answer\n{json_data}\n")

    with open("user_settings.json", "w") as file:
        json.dump(out_put_func, file, ensure_ascii=False, indent=4)

    return json_data


# print(get_json_answer("2021.12.31 16:39:04"))
