import ollama
from typing import List, Tuple
from app.utils.config import settings

def cosine_similarity(A: List[float], B: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    dot_product = sum(a*b for a, b in zip(A, B))
    norm_a = sum(a*a for a in A) ** 0.5
    norm_b = sum(b*b for b in B) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve_p_eta(query: str, top_k: int = 3) -> List[Tuple[str, float]]:
    """Retrieve relevant chunks from knowledge base"""
    try:
        # Get query embedding
        query_embedding = ollama.embed(
            model=settings.EMBEDDING_MODEL,
            input=query
        )['embeddings'][0]
        
        # TODO: Replace with actual vector DB query
        # This is a mock implementation
        similarities = []
        with open('datasets/processed/chunks/chunks.txt', 'r') as f:
            for chunk in f.readlines():
                chunk_embedding = ollama.embed(
                    model=settings.EMBEDDING_MODEL,
                    input=chunk
                )['embeddings'][0]
                similarity = cosine_similarity(query_embedding, chunk_embedding)
                similarities.append((chunk.strip(), similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    except Exception as e:
        raise RuntimeError(f"Retrieval failed: {str(e)}")
