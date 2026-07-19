"""Главный модуль приложения E-commerce."""
from src.models import Product, Category


def main():
    """Основная функция."""
    print("=" * 60)
    print("E-commerce: Управление товарами и категориями")
    print("=" * 60)

    # Создание продуктов через конструктор
    product1 = Product(name="iPhone 15", description="Смартфон от Apple", price=99990.0, quantity=50)
    product2 = Product(name="iPhone 14", description="Предыдущая модель", price=79990.0, quantity=30)

    # Создание продукта через new_product
    product3_dict = {
        'name': 'MacBook Pro 16',
        'description': 'Мощный ноутбук',
        'price': 299990.0,
        'quantity': 15
    }
    product3 = Product.new_product(product3_dict)

    # Создание категорий
    category1 = Category(
        name="Смартфоны",
        description="Мобильные телефоны",
        products=[product1, product2]
    )

    category2 = Category(
        name="Ноутбуки",
        description="Портативные компьютеры",
        products=[product3]
    )

    # Добавление нового продукта через add_product
    product4_dict = {
        'name': 'Dell XPS 15',
        'description': 'Ноутбук от Dell',
        'price': 179990.0,
        'quantity': 20
    }
    product4 = Product.new_product(product4_dict)
    category2.add_product(product4)

    # Вывод информации
    print(f"\n✅ Всего категорий: {Category.total_categories}")
    print(f"✅ Всего продуктов: {Category.total_products}")

    # Вывод информации по категориям с использованием геттера products
    for category in [category1, category2]:
        print(f"\n📦 Категория: {category.name}")
        print(f"   Описание: {category.description}")
        print(f"   Товаров: {len(category.products)}")

        for product_info in category.products:
            print(f"   - {product_info}")

    # Тестирование сеттера цены
    print("\n" + "=" * 60)
    print("Тестирование сеттера цены")
    print("=" * 60)

    print(f"\nСтарая цена iPhone 15: {product1.price} руб.")
    print("Пытаемся установить цену -100...")
    product1.price = -100  # Должно вывести предупреждение
    print(f"Новая цена iPhone 15: {product1.price} руб.")

    print("\n" + "=" * 60)
    print("Программа завершена")
    print("=" * 60)


if __name__ == "__main__":
    main()