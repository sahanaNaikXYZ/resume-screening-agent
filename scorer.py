import math
from typing import List, Dict

def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0:
        return 0.0
    return dot/(na*nb)

def simple_chunk_text(text, chunk_size=512):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i+chunk_size]))
    return chunks

def rank_resumes(jd_embedding, resumes: List[Dict], use_demo=True):
    results = []
    for r in resumes:
        chunks = simple_chunk_text(r["text"], chunk_size=100)
        best_score = 0.0
        best_snip = ""
        for c in chunks:
            emb = None
            if use_demo:
                emb = demo_embed_local(c)
            else:
                from embeddings_client import get_embedding
                emb = get_embedding(c)
            sim = cosine(jd_embedding, emb)
            if sim > best_score:
                best_score = sim
                best_snip = c[:800]
        results.append({
            "filename": r.get("filename","unknown"),
            "score": best_score*100,
            "snippet": best_snip,
            "rationale": "(demo) higher similarity on skills/experience"
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def demo_embed_local(text):
    seed = sum(ord(c) for c in text) % 10000
    import random
    random.seed(seed)
    return [random.random() for _ in range(64)]
