import pytest

from src.utils import hi_message


@pytest.mark.parametrize(
    "time, expected_greeting",
    [
        ("2024.07.03 06:00:00", '"Доброе утро!"'),
        ("2024.07.03 13:00:00", '"Добрый день!"'),
        ("2024.07.03 18:00:00", '"Добрый вечер!"'),
        ("2024.07.03 23:00:00", '"Доброй ночи!"'),
    ],
)
def test_hi_message(time: str, expected_greeting: str) -> None:
    assert hi_message(time) == expected_greeting
