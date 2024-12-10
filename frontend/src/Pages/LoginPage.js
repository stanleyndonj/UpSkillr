// src /pages/LoginPage.js
import React, { useState } from 'react';
import axios from 'axios';
import styles from './LoginPage.module.css';

import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    async function handleLogin(event) {
        event.preventDefault();

        try {
            const response = await axios.post('http://localhost:5000/auth/login', { email, password });
            localStorage.setItem('token', response.data.token);
            navigate('/profile');//Redirect to profile or another page
        } catch (error) {
            setError(error.response?.data?.message || 'Login Failed');
        }
    }
    
    return (
        <div className = "styles.loginPage">
            <h2>Login</h2>
            <form onSubmit={handleLogin} className={styles.form}>
            <input 
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input 
                type="password"
                placeholder="Password"
                value={email}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button type="submit">Login</button>
            {error && <p className={styles.error}>{error}</p>}
            </form>
        </div>
    )

export default LoginPage;

    // NOTE FOR THE TEAM:
// - Integrate the form with a post request to '/auth/login' when the backend is ready
// - Handle the form validation and error messages.