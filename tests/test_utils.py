"""Тесты для модуля utils."""
import pytest
import pandas as pd
from src.utils import load_transactions, filter_by_date_range


def test_load_transactions_success():
    """Тест успешной загрузки транзакций."""
    transactions = load_transactions('data/operations.xlsx')
    assert len(transactions) > 0
    assert 'Дата операции' in transactions[0]


def test_load_transactions_file_not_found():
    """Тест с несуществующим файлом."""
    transactions = load_transactions('nonexistent.xlsx')
    assert transactions == []


def test_filter_by_date_range():
    """Тест фильтрации по датам."""
    transactions = [
        {'Дата операции': '2024-01-15', 'Сумма операции': 100},
        {'Дата операции': '2024-02-15', 'Сумма операции': 200},
        {'Дата операции': '2024-03-15', 'Сумма операции': 300},
    ]
    result = filter_by_date_range(transactions, '2024-01-01', '2024-02-28')
    assert len(result) == 2


def test_filter_by_date_range_empty():
    """Тест с пустым списком."""
    result = filter_by_date_range([], '2024-01-01', '2024-12-31')
    assert result == []