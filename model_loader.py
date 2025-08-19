
from transformers import pipeline
from config import MODEL_NAME, PIPELINE_TASK

def load_model():
    """
    Loads a Hugging Face model based on config.py (PyTorch backend).
    """
    bot = pipeline(PIPELINE_TASK, model=MODEL_NAME, framework="pt")
    return bot

