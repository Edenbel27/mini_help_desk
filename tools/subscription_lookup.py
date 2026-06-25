from data.subscriptions import SUBSCRIPTIONS


def subscription_lookup(customer_id):
    record = SUBSCRIPTIONS.get(customer_id)
    if record is None:
        return {"error": f"No subscription found for {customer_id}"}
    return record