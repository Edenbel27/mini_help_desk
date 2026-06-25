from knowledge.account_kb import ACCOUNT_KNOWLEDGE
from tools.customer_lookup import customer_lookup

def account_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in ACCOUNT_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    personal_keywords = ["my plan", "my account", "my subscription", "what plan", "current plan"]
    if any(kw in msg for kw in personal_keywords):
        state["tools_used"].append("customer_lookup")
        customer = customer_lookup(state["customer_id"])
        if customer and "error" not in customer:
            findings.append(f"Customer record: {customer}")



    state["collected_knowledge"]["account"] = findings
    state["routing_path"].append("account")
    return {"collected_knowledge": {"account": findings}}