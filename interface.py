# interface.py
from model_loader import load_model
from chat_memory import ChatMemory
from config import MODEL_NAME

def run_chat():
    chatbot = load_model()
    memory = ChatMemory()

    print(f"🤖 Chatbot ({MODEL_NAME}) is ready! Type '/exit' to quit.\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() == "/exit":
            print("Exiting chatbot. Goodbye! 👋")
            break

        context = memory.get_context()

        # Adjust prompt depending on model
        if "flan-t5" in MODEL_NAME:
            if context:
                prompt = context + f"\nQuestion: {user_input}\nAnswer:"
            else:
                prompt = f"Question: {user_input}\nAnswer:"
            response = chatbot(prompt, max_new_tokens=100)[0]['generated_text']
        else:  # for GPT-style models
            prompt = context + "\nUser: " + user_input + "\nBot:"
            response = chatbot(
                prompt,
                max_new_tokens=100,
                pad_token_id=50256
            )[0]['generated_text']

            # Extract after "Bot:" for GPT models
            if "Bot:" in response:
                response = response.split("Bot:")[-1].strip()

        bot_reply = response.strip()
        print(f"Bot: {bot_reply}")

        memory.add(user_input, bot_reply)

if __name__ == "__main__":
    run_chat()

