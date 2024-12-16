import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import axios from './axiosConfig';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const verifyToken = useCallback(async (token) => {
    console.log('Starting token verification with token:', token);
    try {
      const response = await axios.get('/auth/verify');
      console.log('Token verification response:', response.data);

      if (response.data.valid) {
        console.log('Token is valid');
        setIsAuthenticated(true);
        setUser(response.data.user);
      } else {
        console.log('Token is invalid');
        logout();
      }
    } catch (error) {
      console.error('Token verification error:', error);
      logout();
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('token');
    console.log('Token from localStorage:', token);
    
    if (token) {
      verifyToken(token);
    } else {
      console.log('No token found');
      setIsLoading(false);
    }
  }, [verifyToken]);

  const login = (userData, token) => {
    console.log('Logging in user:', userData);
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
    setUser(userData);
  };

  const logout = () => {
    console.log('Logging out');
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      user,
      login,
      logout,
      isLoading
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
