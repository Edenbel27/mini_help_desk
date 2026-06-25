import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from langgraph.checkpoint.sqlite import SqliteSaver
from graph.workflow import build_app

load_dotenv()

def run_ticket(message: str, user_id: int) -> str:
    initial_state = {
        "ticket_id": f"T-{user_id}",
        "customer_id": "C-500",   # test customer
        "message": message,
        "domains": [],
        "collected_knowledge": {},
        "routing_path": [],
        "tools_used": [],
    }

    with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
        app = build_app(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": f"T-{user_id}"}}   
        result = app.invoke(initial_state, config=config)

    return result.get("final_response", "Sorry, something went wrong.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    # let the user know we're working (the graph + LLM take a few seconds)
    await update.message.reply_text("Looking into that...")

    # run the (blocking) graph in a thread so the bot stays responsive
    reply = await asyncio.to_thread(run_ticket, user_message, user_id)

    await update.message.reply_text(reply)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Describe your support issue and I'll help or pass it to a human."
    )


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing from .env")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running. Press Ctrl+C to stop.")
    application.run_polling()


if __name__ == "__main__":
    main()