import axios from 'axios';

// Use environment variable if available, or default to the deployed Render URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE || 'https://quantum-coin-api.onrender.com/api',
});

export default api;
