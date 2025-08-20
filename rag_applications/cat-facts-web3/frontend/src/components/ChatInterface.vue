<template>
  <div class="chat-container">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="msg.role">
        <div class="message-content">{{ msg.content }}</div>
        <div v-if="msg.txHash" class="tx-link">
          <a :href="`https://etherscan.io/tx/${msg.txHash}`" target="_blank">
            View transaction
          </a>
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <input
        v-model="currentMessage"
        @keyup.enter="sendMessage"
        placeholder="Ask about cats..."
      />
      <button @click="sendMessage" :disabled="!web3Store.account || isSending">
        {{ isSending ? 'Sending...' : 'Ask' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useWeb3Store } from '../stores/web3Store';

const web3Store = useWeb3Store();
const currentMessage = ref('');
const isSending = ref(false);
const messages = ref([]);

const sendMessage = async () => {
  if (!currentMessage.value.trim() || !web3Store.account) return;
  
  isSending.value = true;
  const userMessage = currentMessage.value;
  messages.value.push({ role: 'user', content: userMessage });
  currentMessage.value = '';
  
  try {
    // Send to blockchain
    const tx = await web3Store.submitQuery(userMessage);
    messages.value.push({ 
      role: 'system', 
      content: 'Processing your question...',
      txHash: tx.transactionHash
    });
    
    // Poll for response (simplified - in real app use events)
    setTimeout(async () => {
      const response = await fetchResponse(tx.transactionHash);
      messages.value.push({ 
        role: 'assistant', 
        content: response.answer 
      });
    }, 5000);
    
  } catch (error) {
    messages.value.push({ 
      role: 'error', 
      content: `Error: ${error.message}`
    });
  } finally {
    isSending.value = false;
  }
};

const fetchResponse = async (txHash) => {
  const response = await fetch(`${import.meta.env.VITE_API_URL}/api/response/${txHash}`);
  return response.json();
};
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
}
.messages {
  margin-bottom: 20px;
}
.message-content {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
}
.user {
  text-align: right;
}
.user .message-content {
  background-color: #e3f2fd;
}
.assistant .message-content {
  background-color: #f5f5f5;
}
.error .message-content {
  background-color: #ffebee;
  color: #c62828;
}
.tx-link {
  font-size: 0.8em;
  color: #666;
}
.input-area {
  display: flex;
  gap: 10px;
}
input {
  flex-grow: 1;
  padding: 10px;
}
button {
  padding: 10px 20px;
}
</style>
