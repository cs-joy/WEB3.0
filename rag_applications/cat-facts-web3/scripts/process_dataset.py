import ollama
from pathlib import Path
from app.web3.ipfs import store_on_ipfs
from app.utils.config import settings

def process_dataset():
    dataset_path = Path('datasets/raw/cat-facts.txt')
    chunks_path = Path('datasets/processed/chunks/chunks.txt')
    embeddings_path = Path('datasets/processed/embeddings/embeddings.txt')
    
    # Read and chunk dataset
    with open(dataset_path, 'r') as f:
        chunks = [line.strip() for line in f if line.strip()]
    
    # Store chunks
    with open(chunks_path, 'w') as f:
        f.write('\n'.join(chunks))
    
    # Generate and store embeddings
    embeddings = []
    for chunk in chunks:
        embedding = ollama.embed(
            model=settings.EMBEDDING_MODEL,
            input=chunk
        )['embeddings'][0]
        embeddings.append(','.join(map(str, embedding)))
    
    with open(embeddings_path, 'w') as f:
        f.write('\n'.join(embeddings))
    
    print(f"Processed {len(chunks)} chunks")
    
    # Upload to IPFS
    chunks_cid = store_on_ipfs('\n'.join(chunks))
    embeddings_cid = store_on_ipfs('\n'.join(embeddings))
    
    print(f"Chunks CID: {chunks_cid}")
    print(f"Embeddings CID: {embeddings_cid}")

if __name__ == '__main__':
    process_dataset()
