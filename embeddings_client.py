import os
import random
from typing import List

def get_embedding(text: str) -> List[float]:
    """Call actual OpenAI embeddings (simple wrapper)."""
    import openai
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = key
    resp = openai.Embedding.create(model="text-embedding-3-small", input=text)
    return resp["data"][0]["embedding"]

def demo_embed(text: str):
    """Return a deterministic pseudo-embedding for demo mode."""
    seed = sum(ord(c) for c in text) % 10000
    random.seed(seed)
    return [random.random() for _ in range(64)]
