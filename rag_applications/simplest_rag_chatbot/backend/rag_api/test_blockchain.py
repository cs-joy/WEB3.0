# test_blockchain.py
import os
import django
import json
from web3 import Web3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rag_api.settings')
django.setup()

# Initialize Web3
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

print(f"Web3 connected: {web3.is_connected()}")
print(f"Chain ID: {web3.eth.chain_id}")
print(f"Latest block: {web3.eth.block_number}")

# Check accounts
if web3.eth.accounts:
    print("Available accounts:")
    for i, account in enumerate(web3.eth.accounts):
        balance = web3.eth.get_balance(account)
        print(f"  {i}: {account} - {web3.from_wei(balance, 'ether')} ETH")

# Load contract
contracts_path = os.path.join(os.path.dirname(__file__), 'contracts')
try:
    with open(os.path.join(contracts_path, 'chatHistory-address.json')) as f:
        contract_address = json.load(f)['ChatHistory']
    print(f"Contract address from file: {contract_address}")
    
    with open(os.path.join(contracts_path, 'ChatHistory.json')) as f:
        contract_abi = json.load(f)['abi']
    
    # Convert to checksum address
    contract_address_checksum = web3.to_checksum_address(contract_address)
    print(f"Checksum address: {contract_address_checksum}")
    
    # Create contract instance
    chat_contract = web3.eth.contract(address=contract_address_checksum, abi=contract_abi)
    
    # Test contract calls
    try:
        chat_count = chat_contract.functions.getChatHistoryCount().call()
        print(f"Total chat entries on blockchain: {chat_count}")
    except Exception as e:
        print(f"Error calling getChatHistoryCount: {e}")
        
    # Test with a specific user
    if web3.eth.accounts:
        test_user = web3.eth.accounts[0]
        checksum_user = web3.to_checksum_address(test_user)
        print(f"Testing with user: {checksum_user}")
        
        try:
            user_chats = chat_contract.functions.getUserChats(checksum_user).call()
            print(f"User chat IDs: {user_chats}")
            
            user_chat_count = chat_contract.functions.getUserChatsCount(checksum_user).call()
            print(f"User chat count: {user_chat_count}")
        except Exception as e:
            print(f"Error calling user functions: {e}")
            
except FileNotFoundError as e:
    print(f"Contract files not found: {e}")
except Exception as e:
    print(f"Error loading contract: {e}")
