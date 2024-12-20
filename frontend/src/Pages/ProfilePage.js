import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ProfilePage.css';
import AIAssistant from '../components/AIAssistant';

function ProfilePage() {
    const [userDetails, setUserDetails] = useState({});
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(true); // Added loading state

    useEffect(() => {
        async function fetchProfile() {
            setIsLoading(true); // Start loading
            try {
                const token = localStorage.getItem('token');
                if (!token) throw new Error('Token is missing. Please log in again.');

                const response = await axios.get('https://upskillr-nis2.onrender.com/api/profile', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setUserDetails(response.data);
            } catch (err) {
                console.error(err); // Log error for debugging
                if (err.response && err.response.data.error) {
                    setError(err.response.data.error); // Display backend error
                } else {
                    setError('Failed to fetch profile details. Please try again.');
                }
            } finally {
                setIsLoading(false); // Stop loading
            }
        }

        fetchProfile();
    }, []);

    return (
        <div className="profile-container">
            <h1>Your Profile</h1>
            <AIAssistant />
            {isLoading ? (
                <p>Loading...</p> // Display loading message
            ) : error ? (
                <p className="error">{error}</p>
            ) : (
                <div className="profile-details">
                    <p><strong>Name:</strong> {userDetails.name}</p>
                    <p><strong>Email:</strong> {userDetails.email}</p>
                    <p><strong>Joined:</strong> {userDetails.joinedDate}</p>
                </div>
            )}
        </div>
    );
}

export default ProfilePage;
