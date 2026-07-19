"""
Тесты для классов Product и Category.
"""
import pytest
from src.models import Product, Category


class TestProduct:
    """Тесты для класса Product."""

    def test_product_initialization(self):
        """Тест корректной инициализации продукта."""
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

    def test_new_product_classmethod(self):
        """Тест создания продукта через new_product."""
        product_dict = {
            'name': 'MacBook Pro',
            'description': 'Ноутбук',
            'price': 199990.0,
            'quantity': 20
        }

        product = Product.new_product(product_dict)

        assert product.name == 'MacBook Pro'
        assert product.description == 'Ноутбук'
        assert product.price == 199990.0
        assert product.quantity == 20

    def test_price_getter(self):
        """Тест геттера цены."""
        product = Product("Товар", "Описание", 100.0, 10)
        assert product.price == 100.0

    def test_price_setter_valid(self):
        """Тест сеттера цены с валидным значением."""
        product = Product("Товар", "Описание", 100.0, 10)
        product.price = 150.0
        assert product.price == 150.0

    def test_price_setter_invalid(self, capsys):
        """Тест сеттера цены с невалидным значением."""
        product = Product("Товар", "Описание", 100.0, 10)
        product.price = -50.0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась

    def test_price_setter_zero(self, capsys):
        """Тест сеттера цены с нулевым значением."""
        product = Product("Товар", "Описание", 100.0, 10)
        product.price = 0

        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 100.0  # Цена не изменилась


class TestCategory:
    """Тесты для класса Category."""

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом."""
        Category.total_categories = 0
        Category.total_products = 0

    def test_category_initialization(self):
        """Тест корректной инициализации категории."""
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
        assert category.description == "Мобильные телефоны"

    def test_add_product(self):
        """Тест добавления продукта через add_product."""
        category = Category(
            name="Смартфоны",
            description="Мобильные телефоны",
            products=[]
        )

        product = Product("iPhone 15", "Смартфон", 99990.0, 50)
        category.add_product(product)

        assert len(category.products) == 1
        assert "iPhone 15" in category.products[0]

    def test_products_property(self):
        """Тест геттера products."""
        products = [
            Product("iPhone 15", "Смартфон", 99990.0, 50),
            Product("iPhone 14", "Смартфон", 79990.0, 30)
        ]

        category = Category(
            name="Смартфоны",
            description="Мобильные телефоны",
            products=products
        )

        products_list = category.products

        assert len(products_list) == 2
        assert "iPhone 15, 99990.0 руб. Остаток: 50 шт." in products_list
        assert "iPhone 14, 79990.0 руб. Остаток: 30 шт." in products_list

    def test_total_categories_count(self):
        """Тест подсчета общего количества категорий."""
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
        """Тест подсчета общего количества продуктов."""
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
            products=[
                Product("Товар 3", "Описание", 300.0, 30)
            ]
        )

        assert Category.total_products == 3

    def test_add_product_updates_total(self):
        """Тест что add_product обновляет total_products."""
        category = Category(
            name="Категория 1",
            description="Описание 1",
            products=[]
        )

        initial_total = Category.total_products

        product = Product("Товар", "Описание", 100.0, 10)
        category.add_product(product)

        assert Category.total_products == initial_total + 1


class TestPrivateAttributes:
    """Тесты для проверки приватности атрибутов."""

    def test_products_is_private(self):
        """Тест что products — приватный атрибут."""
        category = Category(
            name="Категория",
            description="Описание",
            products=[]
        )

        # Проверяем, что __products существует
        assert hasattr(category, '_Category__products')

    def test_price_is_private(self):
        """Тест что price — приватный атрибут."""
        product = Product("Товар", "Описание", 100.0, 10)

        # Проверяем, что __price существует
        assert hasattr(product, '_Product__price')