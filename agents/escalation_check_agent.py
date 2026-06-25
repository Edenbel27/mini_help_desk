def escalation_check_agent(state):

    all_empty = True

    for domain, data in state["collected_knowledge"].items():
        if data:
            all_empty = False

    if all_empty:
        state["escalation_required"] = True
        state["confidence"] = 0.2
        state["escalation_notes"] = "No relevant knowledge found"
    else:
        state["escalation_required"] = False
        state["confidence"] = 0.8
        state["escalation_notes"] = "Sufficient data available"

    state["routing_path"].append("escalation_check")

    return state