"""
Модуль для генерации JSON-ответов для веб-страниц.
"""
import json
from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_greeting(hour: int) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    return "Доброй ночи"


def calculate_cashback(amount: float) -> float:
    """Рассчитывает кешбэк (1 рубль на каждые 100 рублей)."""
    return amount // 100


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют (заглушка)."""
    rates = {
        "USD": 92.5,
        "EUR": 98.3,
        "GBP": 115.2
    }
    return [{"currency": c, "rate": rates.get(c, 0.0)} for c in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций (заглушка)."""
    prices = {
        "AAPL": 175.5,
        "AMZN": 145.2,
        "GOOGL": 140.8,
        "MSFT": 380.1,
        "TSLA": 250.3
    }
    return [{"stock": s, "price": prices.get(s, 0.0)} for s in stocks]


def main_page(
    date_str: str,
    transactions: List[Dict[str, Any]],
    currencies: List[str],
    stocks: List[str]
) -> str:
    """
    Генерирует JSON-ответ для главной страницы.

    Args:
        date_str: Дата и время (YYYY-MM-DD HH:MM:SS)
        transactions: Список транзакций
        currencies: Список валют пользователя
        stocks: Список акций пользователя

    Returns:
        JSON-строка с данными
    """
    logger.info("Генерация главной страницы")

    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        greeting = get_greeting(dt.hour)

        # Группировка по картам
        cards_dict: Dict[str, Dict[str, float]] = {}
        for t in transactions:
            card = str(t.get('Номер карты', ''))
            if not card:
                continue

            if card not in cards_dict:
                cards_dict[card] = {"total": 0.0, "cashback": 0.0}

            amount = float(t.get('Сумма операции', 0) or 0)
            cards_dict[card]["total"] += amount
            cards_dict[card]["cashback"] += calculate_cashback(amount)

        # Формирование списка карт
        cards = []
        for card, info in cards_dict.items():
            last4 = str(card)[-4:] if len(str(card)) >= 4 else str(card)
            cards.append({
                "card": last4,
                "total_amount": round(info["total"], 2),
                "cashback": round(info["cashback"], 2)
            })

        # Топ-5 транзакций по сумме платежа
        sorted_transactions = sorted(
            transactions,
            key=lambda x: float(x.get('Сумма платежа', 0) or 0),
            reverse=True
        )[:5]

        top_transactions = []
        for t in sorted_transactions:
            top_transactions.append({
                "date": str(t.get('Дата операции', '')),
                "amount": round(float(t.get('Сумма платежа', 0) or 0), 2),
                "category": str(t.get('Категория', ''))
            })

        # Формирование ответа
        response = {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": get_currency_rates(currencies),
            "stock_prices": get_stock_prices(stocks)
        }

        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка генерации главной страницы: {e}")
        return json.dumps({"error": str(e)})