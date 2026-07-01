"""
Модуль для генерации JSON-ответов для веб-страницы «Главная».
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, List

import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
STOCK_API_KEY = os.getenv("STOCK_API_KEY", "")


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от текущего локального времени."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def calculate_cashback(amount: float) -> float:
    """Рассчитывает кешбэк (1 рубль на каждые 100 рублей)."""
    return amount // 100


def filter_transactions_by_date(
    transactions: List[Dict[str, Any]],
    date_str: str
) -> List[Dict[str, Any]]:
    """Фильтрует транзакции с начала месяца по указанную дату."""
    try:
        target_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
    except ValueError:
        return []

    start_date = target_date.replace(day=1)

    filtered = []
    for t in transactions:
        try:
            t_date_str = str(t.get('Дата операции', ''))[:10]
            t_date = datetime.strptime(t_date_str, "%Y-%m-%d")
            if start_date <= t_date <= target_date:
                filtered.append(t)
        except (ValueError, TypeError):
            continue

    return filtered


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """Получает курсы валют через API exchangerate-api.com."""
    rates = []

    if not EXCHANGE_API_KEY:
        # Заглушка если нет API ключа
        return [{"currency": c, "rate": 0} for c in currencies]

    for currency in currencies:
        try:
            url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/RUB"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data.get('result') == 'success' and 'conversion_rates' in data:
                    rate = data['conversion_rates'].get(currency, 0)
                    rates.append({
                        "currency": currency,
                        "rate": round(rate, 4) if rate else 0
                    })
                else:
                    rates.append({"currency": currency, "rate": 0})
            else:
                rates.append({"currency": currency, "rate": 0})
        except Exception:
            rates.append({"currency": currency, "rate": 0})

    return rates


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций через API Financial Modeling Prep."""
    prices = []

    if not STOCK_API_KEY:
        # Заглушка если нет API ключа
        return [{"stock": s, "price": 0} for s in stocks]

    for stock in stocks:
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{stock}?apikey={STOCK_API_KEY}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    price = data[0].get('price', 0)
                    prices.append({
                        "stock": stock,
                        "price": round(price, 2) if price else 0
                    })
                else:
                    prices.append({"stock": stock, "price": 0})
            else:
                prices.append({"stock": stock, "price": 0})
        except Exception:
            prices.append({"stock": stock, "price": 0})

    return prices


def main_page(
    date_str: str,
    transactions: List[Dict[str, Any]],
    currencies: List[str],
    stocks: List[str]
) -> str:
    """Генерирует JSON-ответ для главной страницы."""
    greeting = get_greeting()
    filtered_transactions = filter_transactions_by_date(transactions, date_str)

    cards_dict: Dict[str, Dict[str, float]] = {}
    for t in filtered_transactions:
        card = str(t.get('Номер карты', ''))
        if not card:
            continue

        if card not in cards_dict:
            cards_dict[card] = {"total": 0.0, "cashback": 0.0}

        amount = float(t.get('Сумма операции', 0) or 0)
        cards_dict[card]["total"] += amount
        cards_dict[card]["cashback"] += calculate_cashback(amount)

    cards = []
    for card, info in cards_dict.items():
        last4 = card[-4:] if len(card) >= 4 else card
        cards.append({
            "card": last4,
            "total_amount": round(info["total"], 2),
            "cashback": round(info["cashback"], 2)
        })

    sorted_transactions = sorted(
        filtered_transactions,
        key=lambda x: float(x.get('Сумма платежа', 0) or 0),
        reverse=True
    )[:5]

    top_transactions = [
        {
            "date": str(t.get('Дата операции', '')),
            "amount": round(float(t.get('Сумма платежа', 0) or 0), 2),
            "category": str(t.get('Категория', ''))
        }
        for t in sorted_transactions
    ]

    currency_rates = get_currency_rates(currencies)
    stock_prices = get_stock_prices(stocks)

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response, ensure_ascii=False, indent=2)