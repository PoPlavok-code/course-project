"""
Модуль с основными сущностями: Product и Category.
"""
from typing import List


class Product:
    """Класс продукта."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс категории товаров."""

    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        self.name = name
        self.description = description
        self.products = products

        Category.total_categories += 1
        Category.total_products += len(products)