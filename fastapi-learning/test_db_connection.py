from database import get_connection,get_product_by_id, update_product_price, delete_product_by_id, create_product

# print(get_product_by_id(999))

   
# print(update_product_price(7,800.00))

# print(delete_product_by_id(7))

# print(create_product("USB Hub", -799, 5))

# print(get_product_by_id(7))

product_id = create_product("Test Keyboard", 1500, 2)
print(product_id)