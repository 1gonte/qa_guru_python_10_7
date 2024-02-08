import pytest

from models.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(100)

    def test_product_buy(self, product):
        product.buy(500)

        assert product.quantity == 500

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(10000)


class TestCart:

    def test_cart_add_new_product(self, cart, product):
        cart.add_product(product, 5)

        assert cart.products[product] == 5

    def test_cart_add_existing_product(self, cart, product):
        cart.add_product(product, 5)
        cart.add_product(product, 5)

        assert cart.products[product] == 10

    def test_cart_remove_all_product(self, cart, product):
        cart.add_product(product, 5)
        cart.remove_product(product)

        assert product not in cart.products

    def test_cart_remove_some_product(self, cart, product):
        cart.add_product(product, 10)
        cart.remove_product(product, 5)

        assert cart.products[product] == 5

    def test_clear_the_cart(self, cart, product):
        cart.add_product(product)
        cart.clear()

        assert cart.products == {}

    def test_cart_get_total_price(self, cart, product):
        cart.add_product(product, 2)
        expected_total_price = product.price * 2
        total_price = cart.get_total_price()

        assert total_price == expected_total_price

    def test_cart_buy(self, cart, product):
        cart.add_product(product, 500)
        cart.buy()

        assert product.check_quantity(500) and cart.products == {}

    def test_cart_buy_more_than_available(self, cart, product):
        cart.add_product(product, 2000)
        with pytest.raises(ValueError):
            cart.buy()

