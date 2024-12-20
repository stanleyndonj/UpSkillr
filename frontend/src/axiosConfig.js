import axios from 'axios';

const instance = axios.create({
    baseURL: 'https://upskillr-nis2.onrender.com', // Backend URL
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

instance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

instance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (!error.response) {
            console.error('Network or CORS error: Unable to reach the server');
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
