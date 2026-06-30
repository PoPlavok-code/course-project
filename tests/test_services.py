"""Тесты для модуля services."""
import pytest
from src.services import investment_bank


@pytest.fixture
def sample_transactions():
    """Тестовые транзакции."""
    return [
        {
            'Дата операции': '2024-01-15',
            'Сумма операции': 1712.0,
            'Категория': 'Супермаркеты',
            'Описание': 'Пятёрочка'
        },
        {
            'Дата операции': '2024-01-20',
            'Сумма операции': 500.0,
            'Категория': 'Рестораны',
            'Описание': 'Макдоналдс'
        },
        {
            'Дата операции': '2024-02-10',
            'Сумма операции': 1000.0,
            'Категория': 'Супермаркеты',
            'Описание': 'Магнит'
        },
    ]


def test_investment_bank(sample_transactions):
    """Тест расчёта инвесткопилки."""
    result = investment_bank("2024-01", sample_transactions, 50)
    assert result == 38.0


def test_investment_bank_empty():
    """Тест с пустым списком."""
    result = investment_bank("2024-01", [], 50)
    assert result == 0.0