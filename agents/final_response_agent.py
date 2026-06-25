from llm import llm

def final_response_agent(state):

    prompt = f"""
You are a customer support assistant.

Customer message:
{state["message"]}

Knowledge:
{state["collected_knowledge"]}

Confidence: {state["confidence"]}

Escalation:
{state["escalation_required"]}

Write a final helpful response.
"""

    response = llm.invoke(prompt).content

    state["final_response"] = response
    state["routing_path"].append("final")

    return state