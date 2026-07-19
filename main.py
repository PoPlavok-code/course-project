"""Главный модуль приложения E-commerce."""
from src.models import Product, Category


def main():
    """Основная функция."""
    print("=" * 60)
    print("E-commerce: Управление товарами и категориями")
    print("=" * 60)

    product1 = Product(name="iPhone 15", description="Смартфон от Apple", price=99990.0, quantity=50)
    product2 = Product(name="iPhone 14", description="Предыдущая модель", price=79990.0, quantity=30)
    product3 = Product(name="MacBook Pro 16", description="Мощный ноутбук", price=299990.0, quantity=15)

    category1 = Category(name="Смартфоны", description="Мобильные телефоны", products=[product1, product2])
    category2 = Category(name="Ноутбуки", description="Портативные компьютеры", products=[product3])

    print(f"\nВсего категорий: {Category.total_categories}")
    print(f"Всего продуктов: {Category.total_products}")

    for category in [category1, category2]:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        print(f"Товаров: {len(category.products)}")
        for product in category.products:
            print(f"  - {product.name}: {product.price} ₽ ({product.quantity} шт.)")


if __name__ == "__main__":
    main()