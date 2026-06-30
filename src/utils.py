"""
Модуль для загрузки и обработки данных из Excel-файла.
"""
import logging
from typing import List, Dict, Any, cast

import pandas as pd

logger = logging.getLogger(__name__)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel-файла.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        Список словарей с транзакциями
    """
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        df = df.where(pd.notnull(df), None)
        transactions = cast(List[Dict[str, Any]], df.to_dict(orient='records'))
        logger.info(f"Загружено {len(transactions)} транзакций")
        return transactions
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка загрузки: {e}")
        return []


def filter_by_date_range(
    transactions: List[Dict[str, Any]],
    start_date: str,
    end_date: str
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по диапазону дат.

    Args:
        transactions: Список транзакций
        start_date: Начальная дата (YYYY-MM-DD)
        end_date: Конечная дата (YYYY-MM-DD)

    Returns:
        Отфильтрованный список транзакций
    """
    filtered = []
    for t in transactions:
        date = t.get('Дата операции', '')
        if date and start_date <= str(date)[:10] <= end_date:
            filtered.append(t)
    return filtered