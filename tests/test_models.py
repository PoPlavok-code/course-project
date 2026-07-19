"""Тесты для классов Product и Category."""
import pytest
from src.models import Product, Category


class TestProduct:
    def test_product_initialization(self):
        product = Product(
            name="iPhone 15",
            description="Смартфон от Apple",
            price=99990.0,
            quantity=50
        )
        assert product.name == "iPhone 15"
        assert product.description == "Смартфон от Apple"
        assert product.price == 99990.0
        assert product.quantity == 50


class TestCategory:
    def setup_method(self):
        Category.total_categories = 0
        Category.total_products = 0

    def test_category_initialization(self):
        products = [
            Product("iPhone 15", "Смартфон", 99990.0, 50),
            Product("iPhone 14", "Смартфон", 79990.0, 30)
        ]
        category = Category(
            name="Смартфоны",
            description="Мобильные телефоны",
            products=products
        )
        assert category.name == "Смартфоны"
        assert len(category.products) == 2

    def test_total_categories_count(self):
        Category(
            name="Категория 1",
            description="Описание 1",
            products=[Product("Товар 1", "Описание", 100.0, 10)]
        )
        Category(
            name="Категория 2",
            description="Описание 2",
            products=[Product("Товар 2", "Описание", 200.0, 20)]
        )
        assert Category.total_categories == 2

    def test_total_products_count(self):
        Category(
            name="Категория 1",
            description="Описание 1",
            products=[
                Product("Товар 1", "Описание", 100.0, 10),
                Product("Товар 2", "Описание", 200.0, 20)
            ]
        )
        Category(
            name="Категория 2",
            description="Описание 2",
            products=[Product("Товар 3", "Описание", 300.0, 30)]
        )
        assert Category.total_products == 3