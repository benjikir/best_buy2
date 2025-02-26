import pytest
from products import Product  # Assuming the Product class is defined in products.py


def test_create_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True


def test_create_product_invalid_details():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)  # Empty name should raise an exception

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)  # Negative price should raise an exception


def test_product_becomes_inactive_when_quantity_zero():
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=1)
    product.buy(1)  # Buying all the stock
    assert product.quantity == 0
    assert product.is_active() is False


def test_product_buy_modifies_quantity():
    product = Product("Google Pixel 7", price=500, quantity=250)
    result = product.buy(50)
    assert result == 50 * 500  # Should return total price of purchase
    assert product.quantity == 200  # Remaining stock should be 200


def test_buying_more_than_available_raises_exception():
    product = Product("Google Pixel 7", price=500, quantity=10)
    with pytest.raises(ValueError):
        product.buy(20)  # Trying to buy more than available
