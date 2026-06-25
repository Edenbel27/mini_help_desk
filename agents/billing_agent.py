from knowledge.billing_kb import BILLING_KNOWLEDGE

def billing_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in BILLING_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    state["collected_knowledge"]["billing"] = findings
    state["routing_path"].append("billing")

    return {"collected_knowledge": {"billing": findings}}