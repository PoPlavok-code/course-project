class Product:
    """Базовый класс для товаров"""

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __add__(self, other):
        """
        Задание 2: Сложение товаров.
        Разрешаем складывать только объекты одинаковых классов.
        """
        # Используем type() для строгой проверки класса
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        # Возвращаем сумму общей стоимости товаров (цена * количество)
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс-наследник для смартфонов (Задание 1)"""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс-наследник для газонной травы (Задание 1)"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс категории товаров"""

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        # Если список товаров не передан, создаем пустой
        self.products = products if products is not None else []

    def add_product(self, product):
        """
        Задание 3: Защита метода добавления товара.
        Проверяем, что переданный объект является продуктом или его наследником.
        """
        # Используем isinstance() для проверки принадлежности к классу или наследникам
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты класса Product или его наследников")

        self.products.append(product)

    # Дополнительные методы для подсчета категорий и товаров (если были в прошлых ДЗ)
    @classmethod
    def get_category_count(cls):
        return getattr(cls, 'category_count', 0)

    @classmethod
    def get_product_count(cls):
        return getattr(cls, 'product_count', 0)


