"""Тест загрузки данных."""
from src.utils import load_transactions

transactions = load_transactions('data/operations.xlsx')
print(f"Загружено {len(transactions)} транзакций")
if transactions:
    print(f"Первая транзакция: {transactions[0]}")