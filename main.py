from graph.workflow import build_app
from langgraph.checkpoint.sqlite import SqliteSaver
initial_state = {
    "ticket_id": "T-1001",
    "customer_id": "C-500",
    "message": "I am Eden. What plan am I on and when is my next payment due?",

    "category": "",
    "domains": [],

    "collected_knowledge": {},
    "confidence": 0.0,

    "escalation_required": False,
    "escalation_notes": "",

    "final_response": "",

    "routing_path": [],
    "tools_used": []
}

# result = app.invoke(initial_state)

with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    app = build_app(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": initial_state["ticket_id"]}}
    result = app.invoke(initial_state, config=config)


print("\nFINAL RESPONSE:\n")
print(result["final_response"])

print("\nROUTING PATH:\n")
print(result["routing_path"])

print("\nESCALATION NOTES:\n")
print(result["escalation_notes"])

print("\nTOOLS USED:\n")
print(result["tools_used"])