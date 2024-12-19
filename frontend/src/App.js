import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import Navbar from './components/Navbar'; 
import { io } from 'socket.io-client';

// Pages
import HomePage from './Pages/HomePage.js';
import LoginPage from './Pages/LoginPage';
import SignupPage from './Pages/SignupPage';
import ProfilePage from './Pages/ProfilePage';
import Matches from './components/Matches';
import Chat from './components/Chat';
import Reviews from './components/Reviews';

// Utility Components
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  useEffect(() => {
    // Initialize WebSocket connection when the component is mounted
    const socket = io('https://upskillr-1-9xow.onrender.com:10000', {
      transports: ['websocket'], // Use WebSocket transport
      withCredentials: true, // To support sending credentials like cookies
    });

    // Handle socket connection
    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    // Handle messages from the server
    socket.on('message', (data) => {
      console.log('Message from server:', data);
    });

    // Handle errors
    socket.on('connect_error', (err) => {
      console.error('WebSocket connection error:', err);
    });

    // Cleanup WebSocket connection when the component unmounts
    return () => {
      socket.disconnect();
      console.log('WebSocket disconnected');
    };
  }, []); // Empty dependency array to only run once when component mounts

  return (
    <AuthProvider>
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
    </AuthProvider>
  );
}

export default App;
