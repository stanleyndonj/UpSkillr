import React, { useState } from 'react';
import axios from '../axiosConfig';
import styles from './LoginPage.module.css';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'https://upskillr-nis2.onrender.com';

function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth(); 

    async function handleLogin(event) {
        event.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            const response = await axios.post('/auth/login', {
                username,
                password
            }, {
                headers: { 'Content-Type': 'application/json' }
            });
            axios.post('/auth/login', {
                username,
                password
            }, {
                headers: {
                    'Content-Type': 'application/json'
                },
                withCredentials: true 
            });
            
            
            const { token, user } = response.data;
            login(user, token); 

            
            navigate('/profile');
        } catch (error) {
            if (error.response) {
                setError(error.response.data.error || 'Login Failed');
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
            console.error('Login error:', error);
        } finally {
            setIsLoading(false);
        }
    }

    return (
        <div className={styles.loginPage}>
            <h2>Login</h2>
            <form onSubmit={handleLogin} className={styles.form}>
                <input 
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={isLoading}
                />
                <input 
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    disabled={isLoading}
                />
                <button 
                    type="submit"
                    disabled={isLoading}
                >
                    {isLoading ? 'Logging in...' : 'Login'}
                </button>

                {error && <p className={styles.error}>{error}</p>}

                <div className={styles.signup}>
                    <p>
                        Don't have an account? 
                        <span
                            onClick={() => navigate('/signup')}
                            className={styles.signupLink}
                        >
                            {' '}Sign Up
                        </span>
                    </p>
                </div>
            </form>
        </div>
    );
}

export default LoginPage;
