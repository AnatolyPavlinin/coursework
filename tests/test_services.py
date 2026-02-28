import json
from typing import Any, Dict, List
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.services import find_string, get_operations_dict
from src.views import file_path


@patch("pandas.read_excel", create=True)
def test_get_list_of_transactions(mock_read_excel: Mock) -> None:
    mock_read_excel.return_value = pd.DataFrame(
        {
            "Дата операции": ["16.07.2019 16:30:10"],
            "Дата платежа": ["18.07.2019"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-49.8],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-49.8],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [None],
            "Категория": ["Супермаркеты"],
            "MCC": [5411.0],
            "Описание": ["SPAR"],
            "Бонусы (включая кэшбэк)": [0],
            "Округление на инвесткопилку": [0],
            "Сумма операции с округлением": [49.8],
        }
    )

    assert get_operations_dict(file_path) == [
        {
            "MCC": 5411.0,
            "Бонусы (включая кэшбэк)": 0,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "16.07.2019 16:30:10",
            "Дата платежа": "18.07.2019",
            "Категория": "Супермаркеты",
            "Кэшбэк": None,
            "Номер карты": "*7197",
            "Округление на инвесткопилку": 0,
            "Описание": "SPAR",
            "Статус": "OK",
            "Сумма операции": -49.8,
            "Сумма операции с округлением": 49.8,
            "Сумма платежа": -49.8,
        }
    ]


@pytest.fixture
def operations() -> list[dict]:
    return [
        {"Категория": "Еда", "Сумма операции": -100, "Описание": "Магазин"},
        {"Категория": "Транспорт", "Сумма операции": -50, "Описание": "АЗС"},
        {"Категория": "Еда", "Сумма операции": -200, "Описание": "Ресторан"},
    ]


@patch("pandas.read_excel")
def test_find_string(mock_read_excel: Mock, operations: list[dict]) -> None:
    mock_read_excel.return_value = pd.DataFrame(operations)

    result = find_string(file_path, "ресторан")

    expected_result: List[Dict[str, Any]] = []
    assert json.loads(result) == expected_result
    mock_read_excel.assert_called_once_with(file_path)
