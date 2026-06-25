from knowledge.feature_kb import FEATURE_KNOWLEDGE

def feature_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in FEATURE_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    state["collected_knowledge"]["feature"] = findings
    state["routing_path"].append("feature")

    return {"collected_knowledge": {"feature": findings}}