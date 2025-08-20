import json
import os
from web3 import Web3
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatHistory
from .serializers import ChatHistorySerializer
import ollama

# Initialize Web3
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Load contract
contracts_path = os.path.join(settings.BASE_DIR, 'contracts')
with open(os.path.join(contracts_path, 'chatHistory-address.json')) as f:
    contract_address = json.load(f)['ChatHistory']

with open(os.path.join(contracts_path, 'ChatHistory.json')) as f:
    contract_abi = json.load(f)['abi']

chat_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Initialize RAG components
EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

# Load dataset
dataset = []
try:
    with open(settings.DATASET_PATH, 'r') as file:
        dataset = file.readlines()
        print(f'Loaded {len(dataset)} entities')
except FileNotFoundError:
    print("Dataset file not found")

# Vector database
VECTOR_DB = []

def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

for i, chunk in enumerate(dataset):
    add_chunk_to_database(chunk)
    print(f'Added chunk {i+1}/{len(dataset)} to the database')

# Cosine similarity function
def cosine_similarity(A, B):
    dot_product = sum([A_i * B_i for A_i, B_i in zip(A, B)])
    norm_A = sum([A_i ** 2 for A_i in A]) ** 0.5
    norm_B = sum([B_i ** 2 for B_i in B]) ** 0.5
    return dot_product / (norm_A * norm_B) if norm_A * norm_B != 0 else 0

# Retrieval function
def retrieve_p_eta(query_q_x, top_K=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query_q_x)['embeddings'][0]
    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_K]

@api_view(['POST'])
def ask_question(request):
    user_address = request.data.get('user_address')
    query = request.data.get('query')
    
    if not user_address or not query:
        return Response({'error': 'Missing user_address or query'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Retrieve relevant knowledge
    retrieved_knowledge = retrieve_p_eta(query)
    
    # Format context
    chunk_text = '\n'.join([f' - {chunk.strip()}' for chunk, similarity in retrieved_knowledge])
    instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{chunk_text}
'''
    
    # Generate response
    response = ollama.chat(
        model=LANGUAGE_MODEL,
        messages=[
            {'role': 'system', 'content': instruction_prompt},
            {'role': 'user', 'content': query},
        ],
    )
    
    chatbot_response = response['message']['content']
    
    # Store in database
    chat_entry = ChatHistory.objects.create(
        user_address=user_address,
        query=query,
        response=chatbot_response
    )
    
    # Store on blockchain
    try:
        account = web3.eth.accounts[0]  # Using first account for demo
        nonce = web3.eth.get_transaction_count(account)
        
        tx = chat_contract.functions.addChat(query, chatbot_response).build_transaction({
            'chainId': 1337,
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
        
        private_key = "0x..."  # Replace with your private key from Ganache
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        chat_entry.tx_hash = receipt.transactionHash.hex()
        chat_entry.save()
        
    except Exception as e:
        print(f"Error storing on blockchain: {e}")
    
    serializer = ChatHistorySerializer(chat_entry)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_chat_history(request, user_address):
    chats = ChatHistory.objects.filter(user_address=user_address).order_by('-timestamp')
    serializer = ChatHistorySerializer(chats, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_blockchain_history(request, user_address):
    try:
        # Convert address to checksum format
        checksum_address = web3.to_checksum_address(user_address)
        
        # Get user chat IDs from blockchain
        chat_ids = chat_contract.functions.getUserChats(checksum_address).call()
        
        chat_history = []
        for chat_id in chat_ids:
            chat_data = chat_contract.functions.getChatEntry(chat_id).call()
            chat_history.append({
                'user': chat_data[0],
                'query': chat_data[1],
                'response': chat_data[2],
                'timestamp': chat_data[3],
                'id': chat_id
            })
        
        return Response(chat_history)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
