import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'; 

// Pages
import HomePage from './Pages/HomePage.js';
import LoginPage from './Pages/LoginPage';
import SignupPage from './Pages/SignupPage';
import ProfilePage from './Pages/ProfilePage';
import Matches from './components/Matches';
import Chat from './components/Chat';
import Reviews from './components/Reviews';

// Utility Components (e.g., Protected Routes)
import ProtectedRoute from './components/ProtectedRoute';

function App() {
    return (
<Router>
    {/* Navigation bar at the top */}
    <Navbar />
    
    {/* Main Routes */}
    <Routes>
        {/* Public Routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* Protected Routes */}
        <Route 
            path="/profile" 
            element={
            <ProtectedRoute>
            <ProfilePage />
            </ProtectedRoute>
            } 
        />
        <Route 
        path="/matches" 
        element={
            <ProtectedRoute>
            <Matches />
            </ProtectedRoute>
        } 
    />
    <Route 
        path="/chat" 
        element={
        <ProtectedRoute>
            <Chat />
        </ProtectedRoute>
        } 
    />
    <Route 
        path="/reviews" 
        element={
        <ProtectedRoute>
            <Reviews />
        </ProtectedRoute>
        } 
    />
    </Routes>
</Router>
);
}

export default App;
