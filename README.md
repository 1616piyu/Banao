This is a simple command-line chatbot built with Hugging Face’s Transformers library.
It supports:

Instruction-following Q&A using Flan-T5 (factual answers like capitals, math, history, etc.).

Conversation-style chat using models like DialoGPT or Blenderbot.

Short-term memory (remembers last 3–5 turns).

Guardrails for sensitive questions (e.g., names, capitals).

The chatbot runs locally on CPU (GPU optional) and is fully modular.
#project structure
chatbot/
│── config.py         # Select which model to use (Flan-T5, DialoGPT, Blenderbot)
│── model_loader.py   # Loads model & tokenizer
│── chat_memory.py    # Sliding window memory
│── interface.py      # CLI interface (main entry point)
│── README.md         # Documentation

pip install torch transformers  #first load it through your trminal.
 execute codes 

# in config.py change if required
 MODEL_NAME = "google/flan-t5-base"       # best for factual Q&A
# MODEL_NAME = "microsoft/DialoGPT-medium"   # best for conversations
# MODEL_NAME = "facebook/blenderbot-400M-distill"   # general chat
#run the chatbot
python interface.py


VIDEO LINK : https://drive.google.com/file/d/1P2oz57LEal0K37hwJSOK2iZ9X9nowelI/view?usp=drivesdk
