import React, { useEffect, useState } from 'react';
import axios from './axiosConfig'; // Use the configured axios instance
import './ProfilePage.css';

function ProfilePage() {
    const [userDetails, setUserDetails] = useState({});
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchProfile() {
            try {
                setIsLoading(true);
                const response = await axios.get('/api/profile');
                setUserDetails(response.data);
                setError('');
            } catch (err) {
                setError(err.response?.data?.message || 'Failed to fetch profile details. Please try again.');
            } finally {
                setIsLoading(false);
            }
        }

        fetchProfile();
    }, []);

    if (isLoading) {
        return <div className="profile-container">Loading...</div>;
    }

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