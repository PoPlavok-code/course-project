import pytest
from main import Product, Smartphone, LawnGrass, Category


# --- Тесты для Задания 1 (Создание классов) ---
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
    assert isinstance(phone, Product)  # Проверяем наследование


def test_lawngrass_initialization():
    grass = LawnGrass(
        name="Green Grass", description="Lawn", price=500, quantity=20,
        country="Russia", germination_period="14 days", color="Green"
    )
    assert grass.name == "Green Grass"
    assert grass.country == "Russia"
    assert grass.germination_period == "14 days"
    assert grass.color == "Green"
    assert isinstance(grass, Product)  # Проверяем наследование


# --- Тесты для Задания 2 (Сложение товаров) ---
def test_add_same_class_products():
    phone1 = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")
    phone2 = Smartphone("P2", "d", 200, 3, "e", "m", 1, "c")
    # 100*2 + 200*3 = 200 + 600 = 800
    assert phone1 + phone2 == 800


def test_add_different_class_products():
    phone = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")
    grass = LawnGrass("G1", "d", 50, 10, "c", "g", "c")

    # Проверяем, что выбрасывается TypeError
    with pytest.raises(TypeError):
        phone + grass


# --- Тесты для Задания 3 (Защита метода add_product) ---
def test_add_valid_product_to_category():
    category = Category("Electronics", "Devices")
    phone = Smartphone("P1", "d", 100, 2, "e", "m", 1, "c")

    category.add_product(phone)
    assert len(category.products) == 1
    assert category.products[0] == phone


def test_add_invalid_object_to_category():
    category = Category("Electronics", "Devices")

    # Проверяем, что нельзя добавить строку
    with pytest.raises(TypeError):
        category.add_product("Не товар")

    # Проверяем, что нельзя добавить число
    with pytest.raises(TypeError):
        category.add_product(12345)

    # Проверяем, что нельзя добавить обычный список
    with pytest.raises(TypeError):
        category.add_product([])