import axios from 'axios';

axios.defaults.baseURL = 'https://upskillr-nis2.onrender.com';
axios.defaults.withCredentials = true;

const instance = axios.create({
    baseURL: 'https://upskillr-nis2.onrender.com',
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
        // Add CORS headers
       },
    error => {
        return Promise.reject(error);
    }
);

// Enhanced error handling in response interceptor
instance.interceptors.response.use(
    response => response,
    error => {
        if (!error.response) {
            console.error("Network or CORS error: Unable to reach the server");
        } else if (error.response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        } else {
            console.error(`Error ${error.response.status}: ${error.response.data.message || 'Unknown error'}`);
        }
        return Promise.reject(error);
    }
);

export default instance;
