import ollama
from app.utils.config import settings
from typing import List, Tuple

def generate_response(query: str, retrieved_chunks: List[Tuple[str, float]]) -> str:
    """
    Generate response using LLM with retrieved context
    """
    context = "\n".join([chunk for chunk, _ in retrieved_chunks])
    
    prompt = f"""You are a helpful cat facts chatbot. Use only the following context to answer the question.
    
Context:
{context}

Question: {query}
Answer: """
    
    response = ollama.generate(
        model=settings.LANGUAGE_MODEL,
        prompt=prompt,
        stream=False
    )
    
    return response['response']
