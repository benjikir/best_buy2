from typing import List, Tuple
import products


class Store:
    def __init__(self, product_list: List[products.Product]):
        self.product_list = product_list

    def add_product(self, product: products.Product):
        self.product_list.append(product)

    def remove_product(self, product: products.Product):
        self.product_list.remove(product)

    def get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.product_list)

    def get_all_products(self) -> List[products.Product]:
        return [product for product in self.product_list if product.quantity > 0]

    def order(self, shopping_list: List[Tuple[products.Product, int]]) -> float:
        total_price = 0.0
        for product, quantity in shopping_list:
            if product in self.product_list and product.quantity >= quantity:
                product.quantity -= quantity
                total_price += product.price * quantity
            else:
                print(f"Produkt {product.name} ist entweder nicht verfügbar oder die angeforderte Menge ist zu hoch.")
        return total_price


# Beispielprodukte, inkl. Limitierungen und Non-Stocked-Produkte
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
    products.NonStockedProduct("Windows License", price=125),
    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

# Erstelle den Store mit den Produkten
best_buy = Store(product_list)

# Hol alle Produkte, die auf Lager sind
available_products = best_buy.get_all_products()

# Gesamtzahl der Produkte im Store (verfügbar und nicht verfügbar)
print(f"Total Quantity: {best_buy.get_total_quantity()}")

# Bestellung aufgeben: 1 MacBook Air M2, 2 Bose QuietComfort Earbuds
total_cost = best_buy.order([(available_products[0], 1), (available_products[1], 2)])

# Gesamtpreis der Bestellung
print(f"Total cost of order: {total_cost}")
