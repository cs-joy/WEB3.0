from pydantic import BaseModel
from typing import List, Tuple

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    tx_hash: str
    response: str
    ipfs_cid: str
    retrieved_chunks: List[Tuple[str, float]]
