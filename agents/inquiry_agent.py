from knowledge.inquiry_kb import INQUIRY_KNOWLEDGE

def inquiry_agent(state):

    msg = state["message"].lower()
    findings = []

    for k, v in INQUIRY_KNOWLEDGE.items():
        if k in msg:
            findings.append(v)

    state["collected_knowledge"]["inquiry"] = findings
    state["routing_path"].append("inquiry")

    return {"collected_knowledge": {"inquiry": findings}}