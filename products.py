from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class PercentDiscount(Promotion):
    def __init__(self, name: str, percent: float):
        super().__init__(name)
        if percent <= 0 or percent >= 1:
            raise ValueError("Der Rabatt muss zwischen 0 und 1 liegen.")
        self.percent = percent

    def apply_promotion(self, product, quantity):
        """Berechnet den Preis nach Anwendung eines Prozentsatz-Rabatts."""
        return product.price * quantity * (1 - self.percent)


class SecondHalfPrice:
    def __init__(self, name: str):
        self.name = name

    def apply_promotion(self, product, quantity: int) -> float:
        total_price = 0.0
        for i in range(1, quantity + 1):
            if i % 2 == 0:  # Jedes zweite Produkt bekommt den halben Preis
                total_price += product.price / 2
            else:
                total_price += product.price
        return total_price


class ThirdOneFree(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """Berechnet den Preis nach Anwendung des 'Third One Free' Angebots."""
        if quantity < 3:
            raise ValueError("Die Promotion erfordert den Kauf von mindestens 3 Produkten.")
        # Preis für zwei Produkte zahlen, das dritte ist kostenlos
        return product.price * (quantity - quantity // 3)


class Product:
    def __init__(self, name: str, price: float, quantity: int):
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self) -> int:
        return self.quantity

    def set_quantity(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self.quantity > 0

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_promotion(self, promotion: Promotion):
        self.promotion = promotion

    def show(self) -> str:
        promotion_info = f" (Promotion: {self.promotion.name})" if self.promotion else ""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}{promotion_info}"

    def buy(self, quantity: int) -> float:
        if quantity > self.quantity:
            raise ValueError("Nicht genügend Vorrat")
        self.quantity -= quantity
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)  # Promotion anwenden
        else:
            return self.price * quantity

class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    def show(self) -> str:
        return f"{self.name}, Price: {self.price} (Non-Stocked Product)"


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum Purchase: {self.maximum}"


# setup initial stock of inventory
product_list = [
    Product("MacBook Air M2", price=1450, quantity=100),
    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    Product("Google Pixel 7", price=500, quantity=250),
    NonStockedProduct("Windows License", price=125),
    LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

# Create promotion catalog
second_half_price = SecondHalfPrice("Second Half price!")
third_one_free = ThirdOneFree("Third One Free!")
thirty_percent = PercentDiscount("30% off!", percent=0.30)  # Korrektur: 30% Rabatt als 0.30 anstelle von 30

# Add promotions to products
product_list[0].set_promotion(second_half_price)
product_list[1].set_promotion(third_one_free)
product_list[3].set_promotion(thirty_percent)
