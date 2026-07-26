"""
Модуль с основными сущностями: Product и Category.
"""
from typing import List


class Product:
    """
    Класс продукта.

    Attributes:
        name: Название продукта
        description: Описание продукта
        __price: Цена продукта (приватный атрибут)
        quantity: Количество на складе
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализация продукта.

        Args:
            name: Название продукта
            description: Описание продукта
            price: Цена продукта
            quantity: Количество на складе
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """
        Строковое представление продукта.

        Returns:
            Строка в формате: "Название продукта, 80 руб. Остаток: 15 шт."
        """
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        """
        Официальное строковое представление для разработчиков.

        Returns:
            Строка с конструктором объекта
        """
        return f"Product('{self.name}', '{self.description}', {self.__price}, {self.quantity})"

    def __add__(self, other: 'Product') -> float:
        """
        Сложение двух продуктов.
        Возвращает общую стоимость товаров на складе.

        Args:
            other: Другой объект Product

        Returns:
            Сумма стоимостей (price × quantity) обоих продуктов
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")

        return (self.__price * self.quantity) + (other.__price * other.quantity)

    @classmethod
    def new_product(cls, product_dict: dict) -> 'Product':
        """
        Создает объект Product из словаря.

        Args:
            product_dict: Словарь с параметрами продукта

        Returns:
            Объект Product
        """
        return cls(
            name=product_dict['name'],
            description=product_dict['description'],
            price=product_dict['price'],
            quantity=product_dict['quantity']
        )

    @property
    def price(self) -> float:
        """
        Геттер для получения цены.

        Returns:
            Цена продукта
        """
        return self.__price

    @price.setter
    def price(self, value: float):
        """
        Сеттер для установки цены.

        Args:
            value: Новая цена
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


class Category:
    """
    Класс категории товаров.

    Attributes:
        name: Название категории
        description: Описание категории
        __products: Список продуктов в категории (приватный атрибут)

    Class Attributes:
        total_categories: Общее количество категорий
        total_products: Общее количество продуктов
    """

    # Атрибуты класса (общие для всех объектов)
    total_categories: int = 0
    total_products: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Инициализация категории.

        Args:
            name: Название категории
            description: Описание категории
            products: Список продуктов в категории
        """
        self.name = name
        self.description = description
        self.__products = products

        # Обновляем атрибуты класса
        Category.total_categories += 1
        Category.total_products += len(products)

    def __str__(self) -> str:
        """
        Строковое представление категории.

        Returns:
            Строка в формате: "Название категории, количество продуктов: 200 шт."
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product):
        """
        Добавляет продукт в категорию.

        Args:
            product: Объект Product для добавления
        """
        self.__products.append(product)
        Category.total_products += 1

    @property
    def products(self) -> List[str]:
        """
        Геттер для получения списка продуктов.

        Returns:
            Список строк с описанием продуктов
        """
        return [str(product) for product in self.__products]