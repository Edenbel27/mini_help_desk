from graph.workflow import app

initial_state = {
    "ticket_id": "T-1001",
    "customer_id": "C-500",
    "message": "My account was hacked and someone changed my settings",

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

result = app.invoke(initial_state)

print("\nFINAL RESPONSE:\n")
print(result["final_response"])

print("\nROUTING PATH:\n")
print(result["routing_path"])

print("\nESCALATION NOTES:\n")
print(result["escalation_notes"])

print("\nTOOLS USED:\n")
print(result["tools_used"])