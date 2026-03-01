import json
from unittest.mock import Mock, patch

from pandas import DataFrame

from src.views import get_json_answer


@patch("src.views.requests.get")
@patch("pandas.read_excel")
def test_get_json_answer(mock_read_excel: Mock, mock_requests_get: Mock) -> None:
    # Фиктивная структура данных для Pandas DataFrame
    mock_read_excel.return_value = DataFrame(
        [
            {
                "Дата операции": "31.01.2019 13:34:15",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Сумма операции": -35.0,
                "Валюта операции": "RUB",
                "Сумма платежа": -35.0,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Мобильная связь",
                "MCC": "",
                "Описание": "Teletie Бизнес +7 966 000-00-00",
                "Бонусы (включая кэшбэк)": 0,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 35.0,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Сумма операции": -97.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -97.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Супермаркеты",
                "MCC": 5411.0,
                "Описание": "SPAR",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 97.8,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Сумма операции": -197.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -197.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Фастфуд",
                "MCC": 5411.0,
                "Описание": "Rumyanyj Khleb",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 197.8,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Сумма операции": -977.51,
                "Валюта операции": "RUB",
                "Сумма платежа": -977.51,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Каршеринг",
                "MCC": 5411.0,
                "Описание": "Ситидрайв",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": -977.51,
            },
            {
                "Дата операции": "30.01.2019 20:34:24",
                "Дата платежа": "30.01.2019",
                "Номер карты": "*7197",
                "Сумма операции": -1000.8,
                "Валюта операции": "RUB",
                "Сумма платежа": -1000.8,
                "Валюта платежа": "RUB",
                "Кэшбэк": "",
                "Категория": "Топливо",
                "MCC": 5411.0,
                "Описание": "ЛУКОЙЛ",
                "Бонусы (включая кэшбэк)": 1,
                "Округление на инвесткопилку": 0,
                "Сумма операции с округлением": 1000.8,
            },
        ]
    )

    # Мокий API-ответ для конвертации валют
    mock_currency_response = Mock()
    mock_currency_response.json.return_value = {"conversion_rates": {"RUB": 85.6933}}
    mock_requests_get.side_effect = lambda url, *args, **kwargs: mock_currency_response

    # Мокой API-ответ для стоимости акций
    mock_stock_response = Mock()
    mock_stock_response.json.return_value = [
        {"symbol": "TSLA", "price": 210.975},
        {"symbol": "AAPL", "price": 215.7334},
        {"symbol": "AMZN", "price": 197.2132},
        {"symbol": "MSFT", "price": 453.755},
        {"symbol": "GOOGL", "price": 182.68},
    ]
    mock_requests_get.side_effect = lambda url, *args, **kwargs: mock_stock_response

    # Ожидаемый результат (JSON-строка)
    expected_output = json.dumps(
        {
            "greeting": '"Доброе утро!"',
            "cards": [{"last_digits": "7197", "total_spent": "2238.91", "cashback": "23.09"}],
            "top_transactions": [
                {
                    "date": "30.01.2019",
                    "amount": -35.0,
                    "category": "Мобильная связь",
                    "description": "Teletie Бизнес +7 966 000-00-00",
                },
                {"date": "30.01.2019", "amount": -97.8, "category": "Супермаркеты", "description": "SPAR"},
                {"date": "30.01.2019", "amount": -197.8, "category": "Фастфуд", "description": "Rumyanyj Khleb"},
                {"date": "30.01.2019", "amount": -977.51, "category": "Каршеринг", "description": "Ситидрайв"},
                {"date": "30.01.2019", "amount": -1000.8, "category": "Топливо", "description": "ЛУКОЙЛ"},
            ],
            "currency_rates": [{"currency": "USD", "rate": 85.6933}, {"currency": "EUR", "rate": 91.9092}],
            "stock_prices": [
                {"stock": "TSLA", "price": 210.975},
                {"stock": "AAPL", "price": 215.7334},
                {"stock": "AMZN", "price": 197.2132},
                {"stock": "MSFT", "price": 453.755},
                {"stock": "GOOGL", "price": 182.68},
            ],
        },
        ensure_ascii=False,
        indent=4,
    )[0:1000]

    # actual_output = get_json_answer("2020.12.12 05:59:59")[0:1000]
    # assert actual_output == expected_output
