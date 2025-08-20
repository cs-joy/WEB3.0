from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Web3 Configuration
    WEB3_PROVIDER_URL: str
    CONTRACT_ADDRESS: str
    PRIVATE_KEY: str
    QUERY_PRICE: float = 0.01
    
    # IPFS Configuration
    IPFS_API_URL: str = "/ip4/127.0.0.1/tcp/5001"
    IPFS_GATEWAY_URL: str = "https://ipfs.io/ipfs/"
    
    # AI Models
    EMBEDDING_MODEL: str = "hf.co/CompendiumLabs/bge-base-en-v1.5-gguf"
    LANGUAGE_MODEL: str = "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"
    
    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"

settings = Settings()
