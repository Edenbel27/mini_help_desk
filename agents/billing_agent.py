from knowledge.billing_kb import BILLING_KNOWLEDGE
from tools.subscription_lookup import subscription_lookup


def billing_agent(state):
    msg = state["message"].lower()
    findings = []

    # search the billing knowledge base
    for k, v in BILLING_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    # for billing/payment questions, look up the customer's real subscription
    billing_keywords = ["charge", "charged", "bill", "billing", "payment",
                        "invoice", "refund", "subscription", "plan", "price"]
    if any(kw in msg for kw in billing_keywords):
        sub = subscription_lookup(state["customer_id"])
        if "error" not in sub:
            findings.append(f"Subscription record: {sub}")

    return {
        "collected_knowledge": {"billing": findings},
        "routing_path": ["billing"],
        "tools_used": ["billing_kb_search", "subscription_lookup"],
    }