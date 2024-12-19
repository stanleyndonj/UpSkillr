import React, { useState } from 'react';
import axios from 'axios';
import styles from './SignupPage.module.css';
import { useNavigate } from 'react-router-dom';

function SignupPage() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    async function handleSignup(event) {
        event.preventDefault();
        try {
            await axios.post('http://localhost:5000/auth/signup', { username, email, password });
            navigate('/login'); // Redirect to login or another page
        } catch (error) {
            setError(error.response?.data?.error || 'Signup Failed');
        }
    }

    return (
        <div className={styles.signupPage}>
            <h2>Signup</h2>
            <form className={styles.form} onSubmit={handleSignup}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
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
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">Signup</button>
                {error && <p className={styles.error}>{error}</p>}
            </form>
        </div>
    );
}

export default SignupPage;