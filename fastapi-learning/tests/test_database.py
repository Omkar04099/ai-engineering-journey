from database import (get_product_by_id,create_product,update_product_price,delete_product_by_id)
from decimal import Decimal

def test_get_product_by_id():
    product_id = 6
    product = get_product_by_id(product_id)
    assert product is not None
    assert product[1] == "Gaming Mouse"

def test_get_product_by_id_not_found():
    product_id = 9999
    product = get_product_by_id(product_id)
    assert product is None

def test_update_product_price():
    product_id = None
    try:
        product_id = create_product("Blade",500.00,8)
        message = update_product_price(product_id,2500.00)
        assert message == "Product Updated"
        product = get_product_by_id(product_id)
        assert product[2] == Decimal("2500.00")
    finally:
        if product_id is not None:
            delete_product_by_id(product_id)

