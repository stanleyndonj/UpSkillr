import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import axios from './axiosConfig';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    const verifyToken = useCallback(async (token) => {
        console.log('Verifying token...');
        try {
            const response = await axios.get('/auth/verify', {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            
            if (response.data.valid) {
                setIsAuthenticated(true);
                setUser(response.data.user);
            } else {
                logout();
            }
        } catch (error) {
            console.error('Token verification failed:', error.message);
            logout();
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            verifyToken(token);
        } else {
            setIsLoading(false);
        }
    }, [verifyToken]);

    const login = async (userData, token) => {
        try {
            localStorage.setItem('token', token);
            setIsAuthenticated(true);
            setUser(userData);
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    };

    const logout = async () => {
        try {
            await axios.post('/auth/logout');
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('token');
            setIsAuthenticated(false);
            setUser(null);
        }
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