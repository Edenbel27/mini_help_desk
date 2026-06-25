from knowledge.technical_kb import TECHNICAL_KNOWLEDGE

def technical_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in TECHNICAL_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    state["collected_knowledge"]["technical"] = findings
    state["routing_path"].append("technical")

    return {"collected_knowledge": {"technical": findings}}