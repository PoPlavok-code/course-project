"""Тесты для модуля views."""
import json
import pytest
from unittest.mock import patch
from src.views import get_greeting, calculate_cashback, filter_transactions_by_date, main_page


def test_calculate_cashback():
    assert calculate_cashback(1500) == 15.0
    assert calculate_cashback(99) == 0.0
    assert calculate_cashback(100) == 1.0


def test_filter_transactions_by_date():
    transactions = [
        {'Дата операции': '2024-01-15', 'Сумма операции': 100},
        {'Дата операции': '2024-01-20', 'Сумма операции': 200},
        {'Дата операции': '2024-02-15', 'Сумма операции': 300},
    ]
    result = filter_transactions_by_date(transactions, '2024-01-25')
    assert len(result) == 2


def test_filter_transactions_empty():
    result = filter_transactions_by_date([], '2024-01-25')
    assert result == []


@patch('src.views.datetime')
def test_get_greeting_morning(mock_dt):
    mock_dt.now.return_value.hour = 8
    assert get_greeting() == "Доброе утро"


@patch('src.views.get_currency_rates')
@patch('src.views.get_stock_prices')
def test_main_page(mock_stocks, mock_rates):
    mock_rates.return_value = [{"currency": "USD", "rate": 92.5}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 175.5}]

    transactions = [
        {
            'Дата операции': '2024-01-15',
            'Номер карты': '1234',
            'Сумма операции': 1500.0,
            'Сумма платежа': 1500.0,
            'Категория': 'Супермаркеты'
        }
    ]

    result = main_page('2024-01-20', transactions, ['USD'], ['AAPL'])
    data = json.loads(result)

    assert "greeting" in data
    assert "cards" in data
    assert len(data["cards"]) == 1