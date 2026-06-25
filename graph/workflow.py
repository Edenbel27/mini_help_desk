from langgraph.graph import StateGraph, END
from graph.state import SupportState

from agents.triage_agent import triage_agent
from agents.billing_agent import billing_agent
from agents.technical_agent import technical_agent
from agents.feature_agent import feature_agent
from agents.account_agent import account_agent
from agents.inquiry_agent import inquiry_agent
from agents.escalation_check_agent import escalation_check_agent
from agents.escalation_agent import escalation_agent
from agents.final_response_agent import final_response_agent
from langgraph.types import Send

workflow = StateGraph(SupportState)

# nodes
workflow.add_node("triage", triage_agent)
workflow.add_node("billing", billing_agent)
workflow.add_node("technical", technical_agent)
workflow.add_node("feature", feature_agent)
workflow.add_node("account", account_agent)
workflow.add_node("inquiry", inquiry_agent)
workflow.add_node("escalation_check", escalation_check_agent)
workflow.add_node("escalation", escalation_agent)
workflow.add_node("final", final_response_agent)

workflow.set_entry_point("triage")

# routing logic
def route_domains(state):
    mapping = {
        "billing": "billing",
        "technical issue": "technical",
        "feature request": "feature",
        "account management": "account",
        "general inquiry": "inquiry",
    }

    targets = []
    for d in state["domains"]:
        node = mapping.get(d.strip().lower())
        if node and node not in targets:
            targets.append(node)

    if not targets:
        targets = ["inquiry"]

    sends = []
    for node in targets:
        sends.append(Send(node, state))
    return sends

def route_escalation(state):
    return "escalate" if state["escalation_required"] else "resolve"

workflow.add_conditional_edges("triage", route_domains, ["billing", "technical", "feature", "account", "inquiry"])

# domain workers now fan IN directly to escalation_check (aggregator removed)
workflow.add_edge("billing", "escalation_check")
workflow.add_edge("technical", "escalation_check")
workflow.add_edge("feature", "escalation_check")
workflow.add_edge("inquiry", "escalation_check")
workflow.add_edge("account", "escalation_check")

workflow.add_conditional_edges("escalation_check", route_escalation, {
    "escalate": "escalation",
    "resolve": "final"
})

workflow.add_edge("escalation", "final")
workflow.add_edge("final", END)

app = workflow.compile()