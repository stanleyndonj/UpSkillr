// src/axiosConfig.js
import axios from 'axios';

// Set default configuration for Axios
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

// Add an interceptor to include the token in requests
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default axios;