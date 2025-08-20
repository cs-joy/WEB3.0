<template>
  <div>
    <button v-if="!connected" @click="connectWallet">
      Connect Wallet
    </button>
    <div v-else>
      <p>Connected: {{ truncatedAddress }}</p>
      <p>Balance: {{ tokenBalance }} CAT</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useWeb3Store } from '../stores/web3Store';

export default {
  setup() {
    const web3Store = useWeb3Store();
    const connected = ref(false);
    
    const truncatedAddress = computed(() => {
      if (!web3Store.account) return '';
      return `${web3Store.account.slice(0, 6)}...${web3Store.account.slice(-4)}`;
    });
    
    const tokenBalance = computed(() => {
      return web3Store.tokenBalance;
    });
    
    const connectWallet = async () => {
      try {
        await web3Store.connect();
        connected.value = true;
      } catch (error) {
        console.error("Wallet connection failed:", error);
      }
    };
    
    return { connected, truncatedAddress, tokenBalance, connectWallet };
  }
};
</script>
