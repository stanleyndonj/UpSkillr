import axios from 'axios';

// Set default configuration for Axios
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

// Add an interceptor to include the token in requests
const instance = axios.create({
  baseURL: 'http://localhost:5000',
  withCredentials: true,
  headers: {
      'Content-Type': 'application/json'
  }
});

// Add request interceptor for authentication
instance.interceptors.request.use(
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

// Add response interceptor for error handling
instance.interceptors.response.use(
  response => response,
  error => {
      if (!error.response) {
          console.error("Network or CORS error: Check backend or CORS configuration");
      } else {
          console.error(`Error status: ${error.response.status}`, error.response.data);
      }
      return Promise.reject(error);
  }
);

export default instance;