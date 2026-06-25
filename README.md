Customer Support Escalation System

A multi-agent customer support pipeline built on LangGraph. It takes a support ticket,
classifies it, investigates it with one or more specialized agents (in parallel when a
ticket spans several topics), decides whether it can be auto-resolved or needs a human,
and writes the final reply.

System architecture

The workflow is a StateGraph. A ticket enters at triage, fans out to the relevant
domain agents, fans back in to an escalation check, and ends either by going straight to
the final reply or by passing through the escalation agent first.

triage
  │  (route_domains decides which domains apply)
  ├─ billing ──┐
  ├─ technical │   run in parallel — only the matched ones
  ├─ feature   │
  ├─ account   │
  └─ inquiry ──┘
        │  (all feed back into one point)
  escalation_check
        │  escalate? ─ yes ─> escalation ─┐
        └─ no ───────────────────────────┴─> final ─> END

Nine nodes: triage, the five domain specialists, escalation_check, escalation,
and final. The key property is multi-domain handling — a ticket like
"I was charged twice and the app crashes" is both billing and technical, so both agents
run at once and their results are merged before a reply is written.

Agent responsibilities

triage — the only node that runs LLM classification. Reads the message and writes a
list of domains into the state (one or several).

billing / technical / feature / account / inquiry — the specialized resolution
agents. Each owns exactly one category and one knowledge base, searches it for relevant
findings, and returns only its own slice of the result. inquiry also acts as the
default when nothing else matches.

escalation_check — runs after the domain agents finish. Looks at what they found and
decides whether the ticket is auto-resolvable or has to be escalated (e.g. nothing found,
or a sensitive domain came back empty).

escalation — runs only when the check flags it. Calls the customer-lookup tool and
writes handoff notes for a human rep.

final_response — reads the collected knowledge and writes the customer-facing reply,
noting escalation status when relevant.

State design

Every node shares one SupportState. The detail that matters: some fields are written by
multiple agents in parallel, so those fields use reducers that tell LangGraph how to
combine concurrent writes.

pythonfrom typing import TypedDict, List, Dict, Annotated

def merge_dicts(a, b):
    out = dict(a or {})
    out.update(b or {})
    return out

class SupportState(TypedDict):
    ticket_id: str
    customer_id: str
    message: str

    domains: List[str]

    collected_knowledge: Annotated[Dict, merge_dicts]   # written in parallel
    confidence: float

    escalation_required: bool
    escalation_notes: str

    final_response: str

    routing_path: List[str]
    tools_used: List[str]

When billing and technical run together, both write collected_knowledge. A plain field
can only take one write per step, so without a reducer LangGraph raises
InvalidUpdateError. merge_dicts combines the two slices —
{"billing": [...]} and {"technical": [...]} become {"billing": [...], "technical": [...]}.
Because of this, the parallel agents return only the key they change, never the whole
state (returning the whole state would make every field collide on the parallel step).

Routing logic

Two routing functions drive the graph.

route_domains runs after triage and decides which domain agents fire. It returns a
list of Send objects — one per matched domain — and LangGraph runs a list of Sends in
parallel. This is what enables multi-domain tickets; returning a single destination
(as in the original state["domains"][0]) would only ever run one domain.

pythondef route_domains(state):
    mapping = {
        "billing": "billing",
        "technical issue": "technical",
        "feature request": "feature",
        "account management": "account",
        "general inquiry": "inquiry",
    }
    targets = []
    for d in state["domains"]:
        node = mapping.get(d.strip().lower())   # label -> node name, no KeyError
        if node and node not in targets:        # skip unknown, dedupe
            targets.append(node)
    if not targets:
        targets = ["inquiry"]                   # fallback so nothing dead-ends
    return [Send(node, state) for node in targets]

The mapping translates triage's labels ("technical issue") into node names
("technical"); .strip().lower() absorbs LLM casing differences.

route_escalation runs after the escalation check and is a simple two-way branch:

pythondef route_escalation(state):
    return "escalate" if state["escalation_required"] else "resolve"

"escalate" goes to the escalation agent, "resolve" goes straight to final.

Tool integration

Tools live in tools/ as mock lookups over the records in data/. customer_lookup
is called by the escalation agent to attach the customer's record to the handoff notes.
subscription_lookup is available for billing-related questions. The agents decide when
to call them, and anything used is recorded in state["tools_used"].

Persistence strategy

LangGraph persists state through a checkpointer passed to compile(). With one attached,
the full state of every run — including collected_knowledge and the routing path — is
saved per ticket and can be resumed or inspected later. The ticket id is used as the
thread id so each ticket has its own checkpoint history.

To enable SQLite-backed persistence:

pythonfrom langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    app = workflow.compile(checkpointer=checkpointer)
    result = app.invoke(initial_state, config={"configurable": {"thread_id": ticket_id}})

(Requires langgraph-checkpoint-sqlite.) Without a checkpointer, the graph still runs
end to end but keeps no state between runs.
