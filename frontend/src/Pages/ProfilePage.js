import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './ProfilePage.css';

function ProfilePage() {
    const [userDetails, setUserDetails] = useState({});
    const [error, setError] = useState('');

    useEffect(() => {
        async function fetchProfile() {
            try {
                const token = localStorage.getItem('token');
                if (!token) throw new Error('Token is missing. Please log in again.');

                const response = await axios.get('https://upskillr-nis2.onrender.com/api/profile', {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setUserDetails(response.data);
            } catch (err) {
                if (err.response && err.response.data.error) {
                    setError(err.response.data.error); // Display backend error
                } else {
                    setError('Failed to fetch profile details. Please try again.');
                }
            }
        }

        fetchProfile();
    }, []);

    return (
        <div className="profile-container">
            <h1>Your Profile</h1>
            {error ? (
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
