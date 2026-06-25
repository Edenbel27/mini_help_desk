from knowledge.account_kb import ACCOUNT_KNOWLEDGE

def account_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in ACCOUNT_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    state["collected_knowledge"]["account"] = findings
    state["routing_path"].append("account")
    return {"collected_knowledge": {"account": findings}}