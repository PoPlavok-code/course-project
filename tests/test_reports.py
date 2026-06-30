"""Тесты для модуля reports."""
import pytest
import pandas as pd
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday


@pytest.fixture
def sample_df():
    """Тестовый DataFrame."""
    data = {
        'Дата операции': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
        'Категория': ['Супермаркеты', 'Рестораны', 'Супермаркеты', 'Транспорт', 'Рестораны'],
        'Сумма операции': [1500.0, 2300.0, 500.0, 1200.0, 800.0],
        'Описание': ['Пятёрочка', 'Макдоналдс', 'Магнит', 'Метро', 'Кафе']
    }
    return pd.DataFrame(data)


def test_spending_by_category(sample_df):
    """Тест отчёта по категории."""
    result = spending_by_category(sample_df, 'Супермаркеты', '2024-01-20')
    assert len(result) == 2
    assert all(result['Категория'] == 'Супермаркеты') if 'Категория' in result.columns else True


def test_spending_by_category_empty(sample_df):
    """Тест отчёта по несуществующей категории."""
    result = spending_by_category(sample_df, 'Несуществующая', '2024-01-20')
    assert result.empty


def test_spending_by_weekday(sample_df):
    """Тест отчёта по дням недели."""
    result = spending_by_weekday(sample_df, '2024-01-20')
    assert 'День недели' in result.columns
    assert 'Средняя сумма' in result.columns


def test_spending_by_workday(sample_df):
    """Тест отчёта по рабочим/выходным дням."""
    result = spending_by_workday(sample_df, '2024-01-20')
    assert 'Тип дня' in result.columns
    assert 'Средняя сумма' in result.columns