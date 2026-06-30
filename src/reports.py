"""
Модуль отчетов для анализа транзакций.
"""
import pandas as pd
import json
from typing import Optional, Dict, Any, cast
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None):
    """
    Декоратор для сохранения результатов отчета в файл.

    Args:
        filename: Имя файла (опционально). Если не указан, используется имя функции.

    Returns:
        Декоратор
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if filename:
                file_name = filename
            else:
                file_name = f"{func.__name__}_report.json"

            try:
                if isinstance(result, pd.DataFrame):
                    # Конвертируем DataFrame в JSON
                    result.to_json(file_name, orient='records', force_ascii=False, indent=2)
                elif isinstance(result, dict):
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                elif isinstance(result, list):
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                else:
                    logger.warning(f"Неподдерживаемый тип результата: {type(result)}")

                logger.info(f"Отчет сохранен: {file_name}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета: {e}")

            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории
        date: Дата (YYYY-MM-DD), по умолчанию текущая

    Returns:
        DataFrame с тратами по категории
    """
    logger.info(f"Генерация отчета по категории '{category}'")

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date - timedelta(days=90)

    # Фильтрация по дате и категории
    mask = (
            (transactions['Дата операции'] >= start_date.strftime("%Y-%m-%d")) &
            (transactions['Дата операции'] <= end_date.strftime("%Y-%m-%d")) &
            (transactions['Категория'] == category)
    )

    filtered = transactions[mask].copy()

    if filtered.empty:
        logger.warning(f"Не найдено транзакций по категории '{category}'")
        return pd.DataFrame()

    # Конвертируем сумму в float
    filtered['Сумма операции'] = filtered['Сумма операции'].astype(float)

    result = filtered[['Дата операции', 'Сумма операции', 'Описание']]

    total = result['Сумма операции'].sum()
    logger.info(f"Найдено {len(result)} транзакций, общая сумма: {total:.2f}")

    return result


@save_report()
def spending_by_weekday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты по дням недели за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: Дата (YYYY-MM-DD), по умолчанию текущая

    Returns:
        DataFrame со средними тратами по дням недели
    """
    logger.info("Генерация отчета по дням недели")

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date - timedelta(days=90)

    # Фильтрация по дате
    mask = (
            (transactions['Дата операции'] >= start_date.strftime("%Y-%m-%d")) &
            (transactions['Дата операции'] <= end_date.strftime("%Y-%m-%d"))
    )

    filtered = transactions[mask].copy()

    if filtered.empty:
        logger.warning("Не найдено транзакций за указанный период")
        return pd.DataFrame()

    # Конвертируем дату и сумму
    filtered['Дата операции'] = pd.to_datetime(filtered['Дата операции'])
    filtered['Сумма операции'] = filtered['Сумма операции'].astype(float)

    # Добавляем день недели
    filtered['День недели'] = filtered['Дата операции'].dt.day_name()

    # Группируем по дню недели и считаем среднее
    result = filtered.groupby('День недели')['Сумма операции'].mean().reset_index()
    result.columns = ['День недели', 'Средняя сумма']

    # Сортируем по дням недели
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    result['День недели'] = pd.Categorical(result['День недели'], categories=weekday_order, ordered=True)
    result = result.sort_values('День недели')

    logger.info(f"Отчет по дням недели сгенерирован")

    return result


@save_report()
def spending_by_workday(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает средние траты в рабочий и выходной день за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: Дата (YYYY-MM-DD), по умолчанию текущая

    Returns:
        DataFrame со средними тратами по типу дня
    """
    logger.info("Генерация отчета по рабочим/выходным дням")

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date - timedelta(days=90)

    # Фильтрация по дате
    mask = (
            (transactions['Дата операции'] >= start_date.strftime("%Y-%m-%d")) &
            (transactions['Дата операции'] <= end_date.strftime("%Y-%m-%d"))
    )

    filtered = transactions[mask].copy()

    if filtered.empty:
        logger.warning("Не найдено транзакций за указанный период")
        return pd.DataFrame()

    # Конвертируем дату и сумму
    filtered['Дата операции'] = pd.to_datetime(filtered['Дата операции'])
    filtered['Сумма операции'] = filtered['Сумма операции'].astype(float)

    # Определяем тип дня (0-4 = рабочие, 5-6 = выходные)
    filtered['Тип дня'] = filtered['Дата операции'].dt.dayofweek.apply(
        lambda x: 'Рабочий' if x < 5 else 'Выходной'
    )

    # Группируем по типу дня
    result = filtered.groupby('Тип дня')['Сумма операции'].mean().reset_index()
    result.columns = ['Тип дня', 'Средняя сумма']

    # Округляем до 2 знаков
    result['Средняя сумма'] = result['Средняя сумма'].round(2)

    logger.info(f"Отчет по рабочим/выходным дням сгенерирован")

    return result


def get_category_summary(
        transactions: pd.DataFrame,
        date: Optional[str] = None
) -> Dict[str, float]:
    """
    Возвращает сводку по всем категориям за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        date: Дата (YYYY-MM-DD), по умолчанию текущая

    Returns:
        Словарь {категория: общая сумма}
    """
    logger.info("Генерация сводки по категориям")

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_date = end_date - timedelta(days=90)

    # Фильтрация по дате
    mask = (
            (transactions['Дата операции'] >= start_date.strftime("%Y-%m-%d")) &
            (transactions['Дата операции'] <= end_date.strftime("%Y-%m-%d"))
    )

    filtered = transactions[mask].copy()

    if filtered.empty:
        logger.warning("Не найдено транзакций за указанный период")
        return {}

    # Конвертируем сумму
    filtered['Сумма операции'] = filtered['Сумма операции'].astype(float)

    # Группируем по категории
    summary_raw = filtered.groupby('Категория')['Сумма операции'].sum()

    # Округляем значения и преобразуем в dict
    summary = {str(k): round(float(v), 2) for k, v in summary_raw.items()}

    logger.info(f"Найдено {len(summary)} категорий")

    return summary