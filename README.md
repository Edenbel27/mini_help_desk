Customer Support Escalation System

A multi-agent support system built with LangGraph. It takes a support ticket, works out
what it's about, looks up relevant info, and either answers it or escalates it to a human.
A ticket can be about more than one thing (e.g. billing and technical), and those agents
run at the same time.

Architecture

triage -> domain agents (in parallel) -> escalation check -> final reply
                                              |
                                        escalation (if needed)

A ticket starts at triage, goes to one or more domain agents, then to an escalation check,
then to the final reply (passing through the escalation agent first if it needs a human).

Agents


triage – classifies the ticket into one or more domains.
billing / technical / feature / account / inquiry – each searches its own knowledge
base and returns what it finds.
escalation_check – decides if the ticket can be answered automatically or needs a human.
escalation – prepares notes for a human agent.
final_response – writes the reply sent to the customer.


State

All agents share one state object (SupportState). It holds the ticket info, the detected
domains, the knowledge collected by each agent, the escalation flag, and the final response.

Because billing and technical can write to collected_knowledge at the same time, that
field uses a reducer (merge_dicts) so the parallel results combine instead of overwriting
each other.

Routing


route_domains – after triage, sends the ticket to every matching domain agent at once
(returns a list of Send objects, which run in parallel).
route_escalation – after the check, sends the ticket either to the escalation agent
or straight to the final reply.


Tools

Mock lookups in tools/. customer_lookup is used by the escalation agent to fetch the
customer's record. subscription_lookup is available for billing questions.

Persistence

State can be saved using a LangGraph SQLite checkpointer, keyed by ticket id, so runs can be
resumed or inspected. Enable it by passing a checkpointer to compile():

pythonfrom langgraph.checkpoint.sqlite import SqliteSaver

with SqliteSaver.from_conn_string("checkpoints.sqlite") as cp:
    app = workflow.compile(checkpointer=cp)

Run

bashpip install -r requirements.txt
# add GOOGLE_API_KEY to .env
python main.py
