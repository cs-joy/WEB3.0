from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from web3 import Web3
import os
from dotenv import load_dotenv
from app.rag.retrieval import retrieve_p_eta
from app.rag.generation import generate_response
from app.web3.contracts import get_contract, post_query_to_blockchain
from app.web3.ipfs import store_on_ipfs
from app.models.query import QueryRequest, QueryResponse

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/query", response_model=QueryResponse)
async def submit_query(query: QueryRequest):
    """Submit a new query to the chatbot"""
    try:
        # 1. Post question to blockchain
        tx_hash = post_query_to_blockchain(query.question)
        
        # 2. Process with RAG pipeline
        retrieved = retrieve_p_eta(query.question)
        response_text = generate_response(query.question, retrieved)
        
        # 3. Store response on IPFS
        response_cid = store_on_ipfs(response_text)
        
        return {
            "tx_hash": tx_hash,
            "response": response_text,
            "ipfs_cid": response_cid,
            "retrieved_chunks": retrieved
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/response/{tx_hash}")
async def get_response(tx_hash: str):
    """Check response status for a transaction"""
    contract = get_contract()
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    
    if not tx_receipt:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Parse logs to get query ID
    # Implementation depends on your contract events
    
    return {"status": "pending"}  # Simplified for example
