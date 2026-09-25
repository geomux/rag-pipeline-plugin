# embed.py
# Handles embedding with local model. Turns text into a 768-dimensional vector.
import ollama

def embed(text, model):
    return ollama.embed(model=model, input=text)["embeddings"][0]