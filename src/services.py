"""
Модуль сервисов для анализа транзакций.
"""
import math
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def investment_bank(
    month: str,
    transactions: List[Dict[str, Any]],
    limit: int
) -> float:
    """
    Рассчитывает сумму для инвесткопилки.

    Args:
        month: Месяц в формате 'YYYY-MM'
        transactions: Список транзакций
        limit: Предел округления (10, 50 или 100)

    Returns:
        Сумма отложенных средств
    """
    total_saved = 0.0
    for t in transactions:
        date = str(t.get('Дата операции', ''))
        if not date.startswith(month):
            continue
        amount = float(t.get('Сумма операции', 0) or 0)
        if amount <= 0:
            continue
        rounded = math.ceil(amount / limit) * limit
        saved = rounded - amount
        total_saved += saved
    return round(total_saved, 2)


def simple_search(
    transactions: List[Dict[str, Any]],
    query: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по описанию или категории.

    Args:
        transactions: Список транзакций
        query: Строка поиска

    Returns:
        Список найденных транзакций
    """
    query_lower = query.lower()
    results = []
    for t in transactions:
        description = str(t.get('Описание', '') or '').lower()
        category = str(t.get('Категория', '') or '').lower()
        if query_lower in description or query_lower in category:
            results.append(t)
    return results