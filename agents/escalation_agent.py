from tools.customer_lookup import customer_lookup

def escalation_agent(state):

    customer = customer_lookup(state["customer_id"])

    state["escalation_notes"] = f"""
Escalation required for ticket {state["ticket_id"]}.
Customer: {customer}
Issue: {state["message"]}
"""

    state["routing_path"].append("escalation")

    return state