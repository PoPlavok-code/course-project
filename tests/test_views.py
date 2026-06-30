"""Тесты для модуля views."""
import json
import pytest
from src.views import get_greeting, main_page, calculate_cashback


def test_get_greeting_morning():
    """Тест утреннего приветствия."""
    assert get_greeting(8) == "Доброе утро"


def test_get_greeting_afternoon():
    """Тест дневного приветствия."""
    assert get_greeting(14) == "Добрый день"


def test_get_greeting_evening():
    """Тест вечернего приветствия."""
    assert get_greeting(20) == "Добрый вечер"


def test_get_greeting_night():
    """Тест ночного приветствия."""
    assert get_greeting(2) == "Доброй ночи"


def test_calculate_cashback():
    """Тест расчёта кешбэка."""
    assert calculate_cashback(1500) == 15.0
    assert calculate_cashback(99) == 0.0
    assert calculate_cashback(100) == 1.0


def test_main_page():
    """Тест генерации главной страницы."""
    transactions = [
        {
            'Дата операции': '2024-01-15',
            'Номер карты': '1234',
            'Сумма операции': 1500.0,
            'Сумма платежа': 1500.0,
            'Категория': 'Супермаркеты'
        },
        {
            'Дата операции': '2024-01-16',
            'Номер карты': '5678',
            'Сумма операции': 2300.0,
            'Сумма платежа': 2300.0,
            'Категория': 'Рестораны'
        }
    ]

    result = main_page(
        "2024-01-20 14:30:00",
        transactions,
        ["USD", "EUR"],
        ["AAPL"]
    )

    data = json.loads(result)
    assert "greeting" in data
    assert "cards" in data
    assert len(data["cards"]) == 2
    assert "top_transactions" in data
    assert len(data["top_transactions"]) == 2
    assert "currency_rates" in data
    assert "stock_prices" in data


def test_main_page_empty():
    """Тест с пустым списком транзакций."""
    result = main_page(
        "2024-01-20 14:30:00",
        [],
        ["USD"],
        ["AAPL"]
    )
    data = json.loads(result)
    assert data["cards"] == []
    assert data["top_transactions"] == []