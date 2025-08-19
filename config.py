# config.py

# --- Model selection ---
# Good factual Q&A:
MODEL_NAME = "google/flan-t5-base"
PIPELINE_TASK = "text2text-generation"

# You can still try dialogue models later:
# MODEL_NAME = "microsoft/DialoGPT-medium"; PIPELINE_TASK = "text-generation"
# MODEL_NAME = "facebook/blenderbot-400M-distill"; PIPELINE_TASK = "text-generation"

# --- Generation settings (make it deterministic & concise) ---
MAX_NEW_TOKENS = 32
DO_SAMPLE = False       # <- no sampling = fewer silly mistakes
NUM_BEAMS = 1

# --- Memory behavior ---
# For factual Q&A, including history can bias results. Keep it off.
INCLUDE_MEMORY_IN_PROMPT = False

# --- Lightweight safety net for "capital of <country>" questions ---
USE_CAPITAL_GUARDRAIL = True
