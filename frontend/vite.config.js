import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
  },
  server: {
    proxy: {
      '/api' : 'https://quantum-coin-ai.vercel.app/',
    }
    port: 3000,
    historyApiFallback: true
  }
});
