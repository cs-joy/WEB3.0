# API Documentation

## Endpoints

### POST /api/query
Submit a new question to the chatbot

**Request Body:**
```json
{
  "question": "How long do cats sleep?"
}

Response:
{
  "tx_hash": "0x...",
  "response": "On average, cats sleep 2/3 of every day...",
  "ipfs_cid": "Qm...",
  "retrieved_chunks": [
    ["On average cats...", 0.92],
    ["Sleep patterns...", 0.85]
  ]
}

GET /api/response/{tx_hash}

Check response status for a transaction

Response:
{
  "status": "completed",
  "response": "On average cats...",
  "ipfs_cid": "Qm..."
}


## 6. Environment Configuration

### `.env`
```ini
# Backend
WEB3_PROVIDER_URL=http://localhost:8545
CONTRACT_ADDRESS=0xYourContractAddress
PRIVATE_KEY=0xYourPrivateKey
QUERY_PRICE=0.01

# Frontend
VITE_API_URL=http://localhost:8000
VITE_CONTRACT_ADDRESS=0xYourContractAddress
VITE_TOKEN_ADDRESS=0xYourTokenAddress

# Contracts (for hardhat)
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-key
ETHERSCAN_API_KEY=your-key
