import { defineStore } from 'pinia';
import Web3 from 'web3';
import CatTokenABI from '../utils/abis/CatToken.json';

export const useWeb3Store = defineStore('web3', {
  state: () => ({
    web3: null,
    account: null,
    chainId: null,
    tokenBalance: 0,
    contract: null
  }),
  
  actions: {
    async connect() {
      if (window.ethereum) {
        try {
          // Request account access
          const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
          this.web3 = new Web3(window.ethereum);
          this.account = accounts[0];
          
          // Get chain ID
          this.chainId = await this.web3.eth.getChainId();
          
          // Initialize contracts
          await this.initContracts();
          
          // Set up event listeners
          window.ethereum.on('accountsChanged', this.handleAccountsChanged);
          window.ethereum.on('chainChanged', this.handleChainChanged);
          
        } catch (error) {
          console.error("User denied account access", error);
          throw error;
        }
      } else {
        throw new Error("MetaMask not detected");
      }
    },
    
    async initContracts() {
      // Main contract
      const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
      const contractABI = (await import('../utils/abis/AIChatbot.json')).default;
      this.contract = new this.web3.eth.Contract(contractABI, contractAddress);
      
      // Token contract
      const tokenAddress = import.meta.env.VITE_TOKEN_ADDRESS;
      const tokenContract = new this.web3.eth.Contract(CatTokenABI, tokenAddress);
      
      // Get token balance
      this.tokenBalance = await tokenContract.methods.balanceOf(this.account).call();
    },
    
    handleAccountsChanged(accounts) {
      if (accounts.length === 0) {
        // MetaMask is locked or user disconnected
        this.$reset();
      } else {
        this.account = accounts[0];
      }
    },
    
    handleChainChanged(chainId) {
      window.location.reload();
    },
    
    async submitQuery(question) {
      if (!this.contract) throw new Error("Contract not initialized");
      
      const queryPrice = import.meta.env.VITE_QUERY_PRICE;
      const value = this.web3.utils.toWei(queryPrice, 'ether');
      
      return this.contract.methods.postQuery(question)
        .send({ from: this.account, value });
    }
  }
});
