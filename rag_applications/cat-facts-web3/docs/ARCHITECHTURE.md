# Cat Facts Web3 Chatbot Architecture

## Overview
Decentralized chatbot using RAG (Retrieval-Augmented Generation) with Web3 integration.

## Components

### 1. Blockchain Layer
- **Smart Contracts**: 
  - `AIChatbot.sol`: Manages queries and responses
  - `CatToken.sol`: ERC20 token for rewards
- **Ethereum Node**: Ganache for development

### 2. Storage Layer
- **IPFS**: Stores dataset chunks and embeddings
- **Vector Database**: On-chain storage of embeddings (simplified)

### 3. Backend Service
- **FastAPI Server**: 
  - Handles RAG pipeline
  - Interacts with blockchain and IPFS
- **Ollama**: Runs local LLM models

### 4. Frontend
- **Vue.js App**: 
  - Wallet connection (MetaMask)
  - Chat interface
  - Transaction monitoring

## Data Flow
1. User submits question via frontend
2. Question is posted to blockchain
3. Backend processes question with RAG:
   - Retrieves relevant chunks
   - Generates response using LLM
4. Response stored on IPFS
5. Response CID recorded on-chain
6. User rewarded with tokens
