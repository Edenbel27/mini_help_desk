# Mock subscription / payment records, keyed by customer id.

SUBSCRIPTIONS = {
    "C-500": {
        "plan": "Pro",
        "status": "active",
        "billing_cycle": "monthly",
        "price": "$29/month",
        "next_billing_date": "2026-07-01",
        "payment_method": "Visa ending 4242",
        "last_payment": {"date": "2026-06-01", "amount": "$29.00", "status": "paid"},
    },
    "C-501": {
        "plan": "Free",
        "status": "active",
        "billing_cycle": None,
        "price": "$0",
        "next_billing_date": None,
        "payment_method": None,
        "last_payment": None,
    },
    "C-502": {
        "plan": "Enterprise",
        "status": "past_due",
        "billing_cycle": "annual",
        "price": "$2,400/year",
        "next_billing_date": "2026-06-15",
        "payment_method": "Mastercard ending 8888",
        "last_payment": {"date": "2025-06-15", "amount": "$2,400.00", "status": "failed"},
    },
}