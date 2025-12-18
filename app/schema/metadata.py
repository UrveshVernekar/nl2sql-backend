SCHEMA_CONTEXT = """
orders(order_id, order_date, amount, product_id, customer_id)
customers(customer_id, customer_name, region)
products(product_id, product_name, category)

Relationships:
orders.customer_id → customers.customer_id
orders.product_id → products.product_id
"""
