import pytest
from abc import ABC
from main import Product, Smartphone, LawnGrass, Category, BaseProduct, Order, BaseEntity
# --- Тесты для Задания 1 (Абстрактный класс BaseProduct) ---
def test_base_product_is_abstract():
    """Проверяем, что BaseProduct является абстрактным классом"""
    assert issubclass(BaseProduct, ABC)

    # Нельзя создать экземпляр абстрактного класса
    with pytest.raises(TypeError):
        BaseProduct()


def test_product_inherits_from_base_product():
    """Проверяем наследование Product от BaseProduct"""
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, BaseProduct)
    assert issubclass(LawnGrass, BaseProduct)


def test_product_implements_abstract_methods():
    """Проверяем реализацию абстрактных методов"""
    phone = Smartphone("iPhone", "Flagship", 100000, 5, "High", "15 Pro", 256, "Black")

    # Методы должны работать без ошибок
    info = phone.get_product_info()
    assert isinstance(info, str)
    assert "iPhone" in info

    total_cost = phone.calculate_total_cost()
    assert total_cost == 500000  # 100000 * 5


# --- Тесты для Задания 2 (Миксин для логирования) ---
def test_product_logger_mixin(capsys):
    """Проверяем, что миксин печатает информацию о создании объекта"""
    product = Product("Тестовый продукт", "Описание", 100, 10)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "Product(" in captured.out
    assert "Тестовый продукт" in captured.out
    assert "100" in captured.out
    assert "10" in captured.out


def test_smartphone_logger_mixin(capsys):
    """Проверяем логирование для Smartphone"""
    phone = Smartphone("iPhone", "Flagship", 100000, 5, "High", "15 Pro", 256, "Black")

    captured = capsys.readouterr()
    assert "Smartphone(" in captured.out
    assert "iPhone" in captured.out


def test_lawngrass_logger_mixin(capsys):
    """Проверяем логирование для LawnGrass"""
    grass = LawnGrass("Трава", "Газонная", 500, 20, "Россия", "14 дней", "Зеленый")

    captured = capsys.readouterr()
    assert "LawnGrass(" in captured.out
    assert "Трава" in captured.out


# --- Тесты для Дополнительного задания (Класс Order) ---
def test_order_creation():
    """Проверяем создание заказа"""
    phone = Smartphone("iPhone", "Flagship", 100000, 5, "High", "15 Pro", 256, "Black")
    order = Order(phone, 2)

    assert order.product == phone
    assert order.quantity == 2
    assert order.total_cost == 200000  # 100000 * 2


def test_order_inherits_from_base_entity():
    """Проверяем наследование Order от BaseEntity"""
    assert issubclass(Order, BaseEntity)


def test_order_get_entity_info():
    """Проверяем метод get_entity_info для Order"""
    phone = Smartphone("iPhone", "Flagship", 100000, 5, "High", "15 Pro", 256, "Black")
    order = Order(phone, 2)

    info = order.get_entity_info()
    assert "iPhone" in info
    assert "2" in info
    assert "200000" in info


# --- Существующие тесты (не должны сломаться) ---
def test_smartphone_initialization():
    phone = Smartphone(
        name="iPhone 15", description="Flagship", price=100000, quantity=5,
        efficiency="High", model="15 Pro", memory=256, color="Black"
    )
    assert phone.name == "iPhone 15"
    assert phone.efficiency == "High"
    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.color == "Black"
    assert isinstance(phone, Product)


def test_lawngrass_initialization():
    grass = LawnGrass(
        name="Green Grass", description="Lawn", price=500, quantity=20,
        country="Russia", germination_period="14 days", color="Green"
    )
    assert grass.name == "Green Grass"
    assert grass.country == "Russia"
    assert grass.germination_period == "14 days"
    assert grass.color == "Green"
    assert isinstance(grass, Product)


def test_add_same_class_products():
    phone1 = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")
    phone2 = Smartphone("P2", "d", 200, 3, "e", "m", 1, "c")
    assert phone1 + phone2 == 800


def test_add_different_class_products():
    phone = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")
    grass = LawnGrass("G1", "d", 50, 10, "c", "g", "c")

    with pytest.raises(TypeError):
        phone + grass


def test_add_valid_product_to_category():
    category = Category("Electronics", "Devices")
    phone = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")

    category.add_product(phone)
    assert len(category.products) == 1
    assert category.products[0] == phone


def test_add_invalid_object_to_category():
    category = Category("Electronics", "Devices")

    with pytest.raises(TypeError):
        category.add_product("Не товар")

    with pytest.raises(TypeError):
        category.add_product(12345)

    with pytest.raises(TypeError):
        category.add_product([])