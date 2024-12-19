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
    const { login } = useAuth(); // Import login function from AuthContext

    async function handleLogin(event) {
        event.preventDefault();
        setError(''); // Clear any previous error messages
        setIsLoading(true); // Set loading state

        try {
            // Ensure the correct headers and body format
            const response = await axios.post(
                '/auth/login', 
                {
                    username, 
                    password
                }, 
                {
                    headers: { 'Content-Type': 'application/json' }  // Explicitly set the Content-Type to application/json
                }
            );

            // Handle successful login
            const { token, user } = response.data;
            login(user, token); // Update AuthContext with user and token

            // Redirect to profile page
            navigate('/profile');
        } catch (error) {
            // Handle errors (e.g., invalid credentials)
            if (error.response) {
                setError(error.response.data.error || 'Login Failed'); // Display specific error message
            } else {
                setError('An unexpected error occurred. Please try again.'); // General error
            }
            console.error('Login error:', error);
        } finally {
            setIsLoading(false); // Reset loading state after request
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
