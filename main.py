"""Главный модуль приложения E-commerce."""
from src.models import Product, Category


def main():
    """Основная функция."""
    print("=" * 60)
    print("E-commerce: Магические методы")
    print("=" * 60)

    # Создание продуктов
    product1 = Product(name="iPhone 15", description="Смартфон от Apple", price=99990.0, quantity=50)
    product2 = Product(name="iPhone 14", description="Предыдущая модель", price=79990.0, quantity=30)
    product3 = Product(name="MacBook Pro 16", description="Мощный ноутбук", price=299990.0, quantity=15)

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

    # Демонстрация __str__
    print("\n📱 Демонстрация __str__ для Product:")
    print(f"  {product1}")
    print(f"  {product2}")
    print(f"  {product3}")

    print("\n📦 Демонстрация __str__ для Category:")
    print(f"  {category1}")
    print(f"  {category2}")

    # Демонстрация __add__
    print("\n💰 Демонстрация __add__ (сложение продуктов):")
    print(f"  {product1.name}: {product1.price} руб. × {product1.quantity} шт. = {product1.price * product1.quantity} руб.")
    print(f"  {product2.name}: {product2.price} руб. × {product2.quantity} шт. = {product2.price * product2.quantity} руб.")

    total = product1 + product2
    print(f"\n  Сумма: {product1.name} + {product2.name} = {total} руб.")

    # Демонстрация repr
    print("\n🔧 Демонстрация __repr__:")
    print(f"  {repr(product1)}")

    # Итоговая информация
    print("\n" + "=" * 60)
    print(f"✅ Всего категорий: {Category.total_categories}")
    print(f"✅ Всего продуктов: {Category.total_products}")
    print("=" * 60)


if __name__ == "__main__":
    main()