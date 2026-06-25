from llm import llm

def triage_agent(state):

    prompt = f"""
Classify ticket into domains:

Billing, Technical Issue, Feature Request, Account Management, General Inquiry

Ticket:
{state["message"]}

Return comma-separated domains.
"""

    response = llm.invoke(prompt).content

    domains = [d.strip().lower() for d in response.split(",")]

    state["domains"] = domains
    state["routing_path"].append("triage")

    return state