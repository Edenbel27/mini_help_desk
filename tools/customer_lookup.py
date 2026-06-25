from data.customers import CUSTOMERS

def customer_lookup(customer_id):

    return CUSTOMERS.get(
        customer_id,
        {"error": "Customer not found"}
    )