# embed.py
# Handles embedding with local model. Turns text(s) into a 768-dimensional vector.
import ollama

def embed(text: str, model: str) -> list[float]:
    """Embed one text with the local Ollama model and return its vector."""
    return ollama.embed(model=model, input=text)["embeddings"][0]

def embed_batch(texts: list[str], model: str) -> list[list[float]]:
    """Embed many texts in one Ollama call. Returns one vector per text, and keeps the same order."""
    return ollama.embed(model=model, input=texts)["embeddings"]