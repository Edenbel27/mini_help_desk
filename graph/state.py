from typing import TypedDict, List, Dict, Annotated
class SupportState(TypedDict):
    ticket_id: str
    customer_id: str
    message: str

    
    domains: List[str]

    collected_knowledge: Annotated[Dict, merge_dicts]
    confidence: float

    escalation_required: bool
    escalation_notes: str

    final_response: str

    routing_path: List[str]
    tools_used: List[str]

    def merge_dicts(existing: dict, new: dict) -> dict:
        merged = existing.copy()
        merged.update(new)
        return merged