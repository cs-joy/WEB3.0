from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_URL')))
private_key = os.getenv('PRIVATE_KEY')
account = w3.eth.account.from_key(private_key)

# Load contract ABI
with open('../../contracts/abi/AIChatbot.json') as f:
    contract_abi = json.load(f)

contract_address = os.getenv('CONTRACT_ADDRESS')
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def get_contract():
    """Get initialized contract instance"""
    return contract

def post_query_to_blockchain(question: str) -> str:
    """Post a new query to the blockchain"""
    try:
        # Build transaction
        tx = contract.functions.postQuery(question).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 200000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(account.address),
            'value': w3.to_wei(os.getenv('QUERY_PRICE'), 'ether')
        })
        
        # Sign and send
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
    except Exception as e:
        raise RuntimeError(f"Failed to post query: {str(e)}")

def add_response_to_blockchain(query_id: int, response_cid: str) -> str:
    """Add response to a query on-chain"""
    try:
        tx = contract.functions.addResponse(query_id, response_cid).build_transaction({
            'chainId': w3.eth.chain_id,
            'gas': 200000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': w3.eth.get_transaction_count(account.address)
        })
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
    except Exception as e:
        raise RuntimeError(f"Failed to add response: {str(e)}")
