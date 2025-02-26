import pytest
from products import Product, NonStockedProduct, LimitedProduct, SecondHalfPrice, ThirdOneFree, PercentDiscount

def test_create_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() == True

def test_apply_second_half_price_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=3)
    promotion = SecondHalfPrice("Second Half Price")  # Name übergeben
    total_price = promotion.apply_promotion(product, 3)  # Methode geändert zu 'apply_promotion'
    assert total_price == 3625  # Erwarteter Preis nach der Promotion

def test_apply_third_one_free_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=3)
    promotion = ThirdOneFree("Third One Free")  # Name übergeben
    total_price = promotion.apply_promotion(product, 3)  # Methode geändert zu 'apply_promotion'
    assert total_price == 2900  # Erwarteter Preis nach der Promotion

def test_apply_percent_discount_promotion():
    product = Product("MacBook Air M2", price=1450, quantity=3)
    promotion = PercentDiscount("10% Discount", 0.1)  # Name und Prozent übergeben
    total_price = promotion.apply_promotion(product, 3)  # Methode geändert zu 'apply_promotion'
    assert total_price == 3915  # Erwarteter Preis nach der Promotion

def test_apply_invalid_percent_discount():
    with pytest.raises(ValueError):
        PercentDiscount("Invalid Discount", 1.1)  # Rabatt > 1 sollte eine Exception auslösen
    with pytest.raises(ValueError):
        PercentDiscount("Invalid Discount", -0.1)  # Rabatt < 0 sollte eine Exception auslösen

def test_apply_promotion_and_buy():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    promotion = SecondHalfPrice("Second Half Price")
    product.set_promotion(promotion)
    total_price = product.buy(2)  # 2 Produkte gekauft
    assert total_price == 2175  # Erwarteter Preis nach der Promotion

def test_product_list():
    # Überprüfen, ob das Produktlist korrekt ist
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]
    assert len(product_list) == 5

def test_product_becomes_inactive_when_quantity_zero():
    product = Product("MacBook Air M2", price=1450, quantity=0)
    assert not product.is_active()

def test_product_buy_modifies_quantity():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.buy(2)
    assert product.quantity == 98  # Nach dem Kauf von 2 Produkten

def test_buying_more_than_available_raises_exception():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(ValueError):
        product.buy(101)  # Sollte eine Exception werfen, weil mehr gekauft werden soll, als verfügbar ist
