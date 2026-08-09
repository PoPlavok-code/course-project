from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов"""

    @abstractmethod
    def get_product_info(self):
        """Абстрактный метод для получения информации о продукте"""
        pass

    @abstractmethod
    def calculate_total_cost(self):
        """Абстрактный метод для расчета общей стоимости"""
        pass


class ProductLoggerMixin:
    """Миксин для логирования создания объектов"""

    def __init__(self, *args, **kwargs):
        class_name = type(self).__name__
        params = ", ".join([str(arg) for arg in args])
        if kwargs:
            kwargs_str = ", ".join([f"{key}={value}" for key, value in kwargs.items()])
            params = f"{params}, {kwargs_str}" if params else kwargs_str

        print(f"{class_name}({params})")
        super().__init__()


class Product(ProductLoggerMixin, BaseProduct):
    """Базовый класс для товаров"""

    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)

        # Задание 1: Проверка на нулевое количество
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.__price = value

    def get_product_info(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def calculate_total_cost(self):
        return self.price * self.quantity

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """Класс-наследник для смартфонов"""

    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def get_product_info(self):
        return f"{self.name} ({self.model}), {self.price} руб. Остаток: {self.quantity} шт. Цвет: {self.color}, Память: {self.memory}GB"


class LawnGrass(Product):
    """Класс-наследник для газонной травы"""

    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_product_info(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт. Страна: {self.country}, Срок прорастания: {self.germination_period}"


class Category:
    """Класс категории товаров"""

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []

    def add_product(self, product):
        """Защита метода добавления товара"""
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты класса Product или его наследников")
        self.products.append(product)

    # Задание 2: Метод для подсчета среднего ценника
    def get_average_price(self):
        """Подсчитывает средний ценник всех товаров в категории"""
        try:
            total_price = sum(product.price for product in self.products)
            average_price = total_price / len(self.products)
            return average_price
        except ZeroDivisionError:
            # Если в категории нет товаров, возвращаем 0
            return 0


# Дополнительное задание: Класс Order и абстрактный класс для Order и Category
class BaseEntity(ABC):
    """Абстрактный класс для сущностей с именем и описанием"""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def get_entity_info(self):
        """Абстрактный метод для получения информации о сущности"""
        pass


class Order(BaseEntity):
    """Класс заказа"""

    def __init__(self, product, quantity):
        super().__init__(f"Заказ {product.name}", f"Заказ товара {product.name}")
        self.product = product
        self.quantity = quantity
        self.total_cost = product.price * quantity

    def get_entity_info(self):
        return f"Заказ: {self.product.name}, Количество: {self.quantity}, Итого: {self.total_cost} руб."


class CategoryWithEntity(Category, BaseEntity):
    """Категория с наследованием от BaseEntity"""

    def __init__(self, name, description, products=None):
        BaseEntity.__init__(self, name, description)
        Category.__init__(self, name, description, products)

    def get_entity_info(self):
        return f"Категория: {self.name}, Товаров: {len(self.products)}"