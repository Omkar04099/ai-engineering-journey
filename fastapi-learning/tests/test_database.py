from database import (get_product_by_id,create_product,update_product_price,delete_product_by_id)
from decimal import Decimal
import pytest
from psycopg.errors import CheckViolation



def test_get_product_by_id_not_found():
    product_id = 9999
    product = get_product_by_id(product_id)
    assert product is None



def test_create_product():
    product_id = None
    try:
        product_id = create_product("Racing Car",699.45,10)
        assert product_id is not None
        product = get_product_by_id(product_id)
        assert product is not None
        assert product[1] == "Racing Car"
        assert product[2] == Decimal("699.45")
        assert product[3] == 10
    finally:
        if product_id is not None:
            delete_product_by_id(product_id)


def test_create_product_invalid():
    with pytest.raises(CheckViolation):
        create_product("Gaming Laptop",-120343.54,45)



def test_delete_product_by_id_invalid():
    product_id = 9999
    message = delete_product_by_id(product_id)
    assert message == f"Product not found with product_id: {product_id}"

@pytest.fixture
def temporary_product():
    product_id = create_product("Laptop Charger",450.69,40)
    yield product_id
    delete_product_by_id(product_id)
    assert get_product_by_id(product_id) is None

def test_temporary_product_exist(temporary_product):
    assert temporary_product is not None
    product = get_product_by_id(temporary_product)
    assert product is not None
    assert product[1] == "Laptop Charger"


def test_update_product_price(temporary_product):
    message = update_product_price(temporary_product,2500.00)
    assert message == "Product Updated"
    product = get_product_by_id(temporary_product)
    assert product[2] == Decimal("2500.00")

def test_update_product_price_not_found():
    message = update_product_price(9999,2546.45)
    assert message == f"Product not found for product_id: 9999"

def test_get_product_by_id(temporary_product):
    product = get_product_by_id(temporary_product)
    assert product is not None
    assert product[1] == "Laptop Charger"


def test_delete_product_by_id(temporary_product):
    message = delete_product_by_id(temporary_product)
    assert message == "Product deleted successfully"
        
    non_existing_product = get_product_by_id(temporary_product)
    assert non_existing_product is None
   