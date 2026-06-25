# Customer Support Escalation System

A multi-agent support system built with LangGraph. It takes a support ticket, works out
what it's about, looks up relevant info, and either answers it or escalates it to a human.
A ticket can be about more than one thing (e.g. billing *and* technical), and those agents
run at the same time. You can interact with it either by running a single ticket from the
command line, or by chatting with a Telegram bot.

## Architecture

```
triage -> domain agents (in parallel) -> escalation check -> final reply
                                              |
                                        escalation (if needed)
```

A ticket starts at triage, goes to one or more domain agents, then to an escalation check,
then to the final reply (passing through the escalation agent first if it needs a human).

## Agents

- **triage** – classifies the ticket into one or more domains.
- **billing / technical / feature / account / inquiry** – each handles its own category.
  They search their knowledge base and, where relevant, call tools to look up the
  customer's real data.
- **escalation_check** – decides if the ticket can be answered automatically or needs a human.
- **escalation** – prepares notes for a human agent.
- **final_response** – writes the reply sent to the customer.

## State

All agents share one state object (`SupportState`). It holds the ticket info, the detected
domains, the knowledge collected by each agent, the escalation flag, and the final response.
It also tracks `routing_path` and `tools_used` so you can see how each ticket was handled.

Because billing and technical can write to `collected_knowledge` at the same time, that
field uses a reducer (`merge_dicts`) so the parallel results combine instead of overwriting
each other. For this to work, each domain agent returns only the part of the state it
changes, not the whole thing.

## Routing

- **route_domains** – after triage, sends the ticket to every matching domain agent at once
  (returns a list of `Send` objects, which run in parallel).
- **route_escalation** – after the check, sends the ticket either to the escalation agent
  or straight to the final reply.

## Tools

Mock lookups in `tools/`, backed by data in `data/`:

- **customer_lookup** – fetches the customer's profile record.
- **subscription_lookup** – fetches the customer's plan and payment details (used for
  billing and plan questions).

Agents call these when a question needs the customer's actual data rather than a generic
knowledge-base answer. Anything used is recorded in `state["tools_used"]`.

## Interfaces

**Command line** – `main.py` runs a single hardcoded ticket through the graph and prints
the final response, routing path, escalation notes, and tools used. Useful for testing.

**Telegram bot** – `telegram_bot.py` lets a user chat with the system. Each message becomes
a ticket, runs through the same graph, and the reply is sent back in the chat.

## Run

```bash
pip install -r requirements.txt
```

Add your keys to `.env`:

```
GOOGLE_API_KEY=your_gemini_key
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
```

Run a single ticket from the command line:

```bash
python main.py
```

Or start the Telegram bot and message it on Telegram:

```bash
python telegram_bot.py
```
