"""Создание тестовых данных для курсовой работы."""
import pandas as pd
from datetime import datetime, timedelta
import random

# Генерируем тестовые транзакции
categories = [
    "Супермаркеты", "Рестораны", "Транспорт", "Развлечения",
    "Медицина", "Одежда", "Топливо", "Кафе", "Кинотеатры", "Переводы"
]

transactions = []
start_date = datetime(2024, 1, 1)

for i in range(50):
    date = start_date + timedelta(days=i)
    category = random.choice(categories)
    amount = round(random.uniform(100, 5000), 2)

    transactions.append({
        "Дата операции": date.strftime("%Y-%m-%d"),
        "Дата платежа": date.strftime("%Y-%m-%d"),
        "Номер карты": f"{random.randint(1000, 9999)}",
        "Статус": "OK" if random.random() > 0.1 else "FAILED",
        "Сумма операции": amount,
        "Валюта операции": "RUB",
        "Сумма платежа": amount,
        "Валюта платежа": "RUB",
        "Кешбэк": round(amount * 0.01, 2),
        "Категория": category,
        "MCC": random.randint(1000, 9999),
        "Описание": f"Оплата: {category}",
        "Бонусы (включая кешбэк)": random.randint(0, 100),
        "Округление на «Инвесткопилку»": round(random.uniform(0, 50), 2),
        "Сумма операции с округлением": round(amount + random.uniform(0, 50), 2),
    })

df = pd.DataFrame(transactions)
df.to_excel("data/operations.xlsx", index=False, engine="openpyxl")

print(f"✅ Создан файл data/operations.xlsx")
print(f"📊 Строк: {len(df)}")
print(f"📋 Колонки: {list(df.columns)}")