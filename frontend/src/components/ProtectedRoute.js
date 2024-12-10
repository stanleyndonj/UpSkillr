import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
// Simulate user authentication (replace with backend logic)
    const isAuthenticated = !!localStorage.getItem('token'); 

// Redirect to login if not authenticated
    return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
