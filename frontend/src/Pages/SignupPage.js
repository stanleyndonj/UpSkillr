// src/pages/Signup.js
import React ,{ useState } from 'react';
import axios from 'axios';
import styles from './SignupPage.module.css';
import {useNavigate} from 'react-router-dom';

function SignupPage(){
    const [name,setName]=useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    async function handleSignup(event) {
        event.preventDefault();
        try {
            await axios.post('http://localhost:5000/auth/signup', { email, password });
            navigate('/login');//Redirect to login or another page
        } catch (error) {
            setError(error.response?.data?.message || 'Signup Failed');
        }
    }

    return (
        <div className = {styles.signupPage}>
            <h2>Signup</h2>
            <form  className={styles.form} onSubmit={handleSignup}>
            <input 
                type="name"
                placeholder="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
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
    )
}

export default SignupPage;


// NOTE FOR THE TEAM:
// - Integrate the form with a post request to '/auth/signup' when the backend is ready
// - Handle the form validation and error messages.
// - Redirect the user to the login page after successful signup.
