"""
Главный модуль приложения.
"""
import sys
import os
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_transactions
from src.views import main_page
from src.services import investment_bank, simple_search
from src.reports import spending_by_category

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main() -> None:
    """Основная функция приложения."""
    print("=" * 60)
    print("Приложение для анализа транзакций")
    print("=" * 60)

    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN"]
        }

    file_path = 'data/operations.xlsx'
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден!")
        return

    transactions = load_transactions(file_path)
    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    print(f"\nЗагружено {len(transactions)} транзакций")

    while True:
        print("\n" + "=" * 60)
        print("Меню:")
        print("1. Главная страница")
        print("2. Инвесткопилка")
        print("3. Простой поиск")
        print("4. Отчет по категории")
        print("0. Выход")
        print("=" * 60)

        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            date_input = input("Введите дату (YYYY-MM-DD): ").strip()
            if not date_input:
                date_input = datetime.now().strftime("%Y-%m-%d")

            result = main_page(
                date_input,
                transactions,
                settings["user_currencies"],
                settings["user_stocks"]
            )
            print("\n" + result)

        elif choice == "2":
            month = input("Введите месяц (YYYY-MM): ").strip()
            limit = int(input("Введите предел округления (10, 50, 100): ").strip())
            saved = investment_bank(month, transactions, limit)
            print(f"\nСумма в инвесткопилке за {month}: {saved} руб.")

        elif choice == "3":
            query = input("Введите строку для поиска: ").strip()
            results = simple_search(transactions, query)
            print(f"\nНайдено {len(results)} транзакций:")
            for t in results[:10]:
                print(f"- {t.get('Дата операции')}: {t.get('Описание')}")

        elif choice == "4":
            import pandas as pd
            df = pd.DataFrame(transactions)
            category = input("Введите категорию: ").strip()
            result = spending_by_category(df, category)
            print(f"\nТраты по категории '{category}':")
            print(result)

        elif choice == "0":
            print("\nДо свидания!")
            break

        else:
            print("\nНеверный выбор!")


if __name__ == "__main__":
    main()