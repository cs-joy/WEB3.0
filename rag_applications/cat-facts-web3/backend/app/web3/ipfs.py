import ipfshttpclient
import os
from dotenv import load_dotenv
from app.utils.logger import logger

load_dotenv()

class IPFSClient:
    def __init__(self):
        self.client = ipfshttpclient.connect(os.getenv('IPFS_API_URL'))
    
    def store_text(self, text: str) -> str:
        """Store text data on IPFS and return CID"""
        try:
            res = self.client.add_str(text)
            return res
        except Exception as e:
            logger.error(f"IPFS store failed: {str(e)}")
            raise
    
    def retrieve_text(self, cid: str) -> str:
        """Retrieve text data from IPFS using CID"""
        try:
            res = self.client.cat(cid)
            return res.decode('utf-8')
        except Exception as e:
            logger.error(f"IPFS retrieve failed: {str(e)}")
            raise

ipfs_client = IPFSClient()

def store_on_ipfs(data: str) -> str:
    return ipfs_client.store_text(data)

def get_from_ipfs(cid: str) -> str:
    return ipfs_client.retrieve_text(cid)
