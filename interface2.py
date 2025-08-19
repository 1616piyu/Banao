# interface.py
import re
from model_loader import load_model
from chat_memory import ChatMemory
from config import (
    MODEL_NAME, PIPELINE_TASK, MAX_NEW_TOKENS, DO_SAMPLE, NUM_BEAMS,
    INCLUDE_MEMORY_IN_PROMPT, USE_CAPITAL_GUARDRAIL
)

# Minimal lookup used only if the model slips on obvious facts.
COMMON_CAPITALS = {
    "france": "Paris",
    "italy": "Rome",
    "india": "New Delhi",
    "germany": "Berlin",
    "spain": "Madrid",
    "japan": "Tokyo",
    "china": "Beijing",
    "russia": "Moscow",
    "united kingdom": "London",
    "uk": "London",
    "united states": "Washington, D.C.",
    "usa": "Washington, D.C.",
    "canada": "Ottawa",
    "australia": "Canberra",
    "brazil": "Brasília",
}

def capital_guardrail(user_text: str):
    """
    If the user asks "capital of X", return a trusted capital if we have it.
    Otherwise return None and let the model answer.
    """
    m = re.search(r"capital of\s+([a-zA-Z .'-]+)\??", user_text.strip().lower())
    if not m:
        return None
    country = m.group(1).strip()
    # normalize common prefixes
    if country.startswith("the "):
        country = country[4:]
    return COMMON_CAPITALS.get(country)

def build_prompt(memory_text: str, user_input: str) -> str:
    """
    Build a clean instruction-style prompt for Flan-T5 models.
    Keep it short and directive to reduce drift.
    """
    header = "You are a helpful factual assistant. Answer correctly and briefly.\n"
    if INCLUDE_MEMORY_IN_PROMPT and memory_text:
        return (
            header
            + "Previous Q&A (for context only, do not copy past answers):\n"
            + memory_text
            + f"\nQuestion: {user_input}\nAnswer:"
        )
    else:
        return header + f"Question: {user_input}\nAnswer:"

def run_chat():
    chatbot = load_model()
    memory = ChatMemory(max_turns=5)

    print(f"🤖 Chatbot ({MODEL_NAME}) is ready! Type '/exit' to quit.\n")

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "/exit":
            print("Exiting chatbot. Goodbye! 👋")
            break

        # 1) Guardrail for obvious "capital of X" questions (optional but reliable)
        if USE_CAPITAL_GUARDRAIL:
            guarded = capital_guardrail(user_input)
            if guarded:
                bot_reply = guarded
                print(f"Bot: {bot_reply}")
                memory.add(user_input, bot_reply)
                continue

        # 2) Build prompt
        context = memory.get_context()
        if "flan-t5" in MODEL_NAME:
            prompt = build_prompt(context, user_input)

            # Deterministic generation for factual queries
            out = chatbot(
                prompt,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=DO_SAMPLE,
                num_beams=NUM_BEAMS,
            )[0]["generated_text"]

            bot_reply = out.strip()
        else:
            # Fallback for GPT-style dialogue models (if you switch models in config)
            prompt = (context + "\n" if context else "") + f"User: {user_input}\nBot:"
            out = chatbot(
                prompt,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=DO_SAMPLE,
                num_beams=NUM_BEAMS,
                pad_token_id=50256,
            )[0]["generated_text"]
            bot_reply = out.split("Bot:")[-1].strip() if "Bot:" in out else out.strip()

        print(f"Bot: {bot_reply}")
        memory.add(user_input, bot_reply)

if __name__ == "__main__":
    run_chat()
