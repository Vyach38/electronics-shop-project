import os
import csv


class Item:
    """
    Класс для представления товара в магазине.
    """
    pay_rate = 1.0
    all = []
    csv_file = os.path.join(os.path.dirname(__file__), "items.csv")

    def __init__(self, name: str, price: float, quantity: int) -> None:
        """
        Создание экземпляра класса item.

        :param name: Название товара.
        :param price: Цена за единицу товара.
        :param quantity: Количество товара в магазине.
        """
        super().__init__()  # вызываем чтобы инициализатор перешел в класс-миксин (MixinLang)
        self.__name = name
        self.price = price
        self.quantity = quantity
        Item.all.append(self)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.__name}', {self.price}, {self.quantity})"

    @classmethod
    def instantiate_from_csv(cls):
        """Открываем файл items.csv для чтения, с помощью модуля "csv" и метода "DictReader" делаем итерацию по нему и
        в каждой итерации создаем новый экземпляр класса item
        """
        cls.all = []
        try:
            with open(Item.csv_file, newline="", encoding="latin-1") as file:
                read_file = csv.DictReader(file)
                for product in read_file:
                    name = product['name']
                    price = product['price']
                    quantity = product['quantity']
                    item = cls(name, float(price), int(quantity))
        except FileNotFoundError:
            print("FileNotFoundError: Отсутствует файл item.csv")
        except KeyError:
            raise InstantiateCSVError from None
        else:
            return item

    @staticmethod
    def string_to_number(arg: str) -> int:
        """Преобразует строковое число в int()"""
        if arg.isdigit():
            return int(arg)
        elif arg.count(".") == 1:
            b = float(arg)
            return int(b)
        else:
            raise ValueError("Не возможно преобразовать в число десятичной системы счисления ")

    @property
    def name(self) -> str:
        """Возвращает имя экземпляра класса"""
        return self.__name

    @name.setter
    def name(self, name: str) -> str:
        """Изменяет имя экземпляра класса"""
        self.__name = name
        if len(self.__name) > 10:
            raise Exception("Не допустимо длинное название товара")
        else:
            return self.__name

    def calculate_total_price(self) -> float:
        """
        Рассчитывает общую стоимость конкретного товара в магазине.

        :return: Общая стоимость товара.
        """
        return float(self.price * self.quantity)

    def apply_discount(self) -> None:
        """
        Применяет установленную скидку для конкретного товара.
        """
        self.price *= Item.pay_rate

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.quantity + other.quantity
        else:
            return None


class InstantiateCSVError(Exception):
    """В этом классе мы переопределяем сообщение в родительском классе Exception"""
    def __init__(self, massage="Файл item.csv поврежден"):
        super().__init__(massage)
        self.massage = massage
