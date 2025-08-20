import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  define: {
    'process.env': {
      VITE_API_URL: JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8000'),
      VITE_CONTRACT_ADDRESS: JSON.stringify(process.env.VITE_CONTRACT_ADDRESS),
      VITE_TOKEN_ADDRESS: JSON.stringify(process.env.VITE_TOKEN_ADDRESS),
      VITE_QUERY_PRICE: JSON.stringify(process.env.VITE_QUERY_PRICE || '0.01')
    }
  }
})
