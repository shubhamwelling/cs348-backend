// src/App.js
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Navigation from './components/Navigation';
import './App.css';
import CombinedList from './components/CombinedCustomerOrderListPage';
import Report from './components/Report';
import AddCustomerPage from './components/AddCustomer';
import UpdateCustomer from './components/UpdateCustomer';
import UpdateOrder from './components/UpdateOrder';
import AddOrder from './components/AddOrder';
import HomePage from './components/HomePage';
import axios from 'axios';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                await axios.get('https://cs348-backend-a1eh.onrender.com/auth/me', { withCredentials: true });
                setIsAuthenticated(true);
            } catch (error) {
                setIsAuthenticated(false);
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return isAuthenticated ? (
        <>
            <Navigation />
            {children}
        </>
    ) : <Navigate to="/login" />;
};

function App() {
    return (
        <Router>
            <div className="container">
                <h1>Dunder Mifflin Order Management System</h1>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/" element={<Navigate to="/login" />} />
                    <Route 
                        path="/home" 
                        element={
                            <ProtectedRoute>
                                <HomePage />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/records" 
                        element={
                            <ProtectedRoute>
                                <CombinedList />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/customers/add" 
                        element={
                            <ProtectedRoute>
                                <AddCustomerPage />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/customers/update/:id" 
                        element={
                            <ProtectedRoute>
                                <UpdateCustomer />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/orders/add" 
                        element={
                            <ProtectedRoute>
                                <AddOrder />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/orders/update/:id" 
                        element={
                            <ProtectedRoute>
                                <UpdateOrder />
                            </ProtectedRoute>
                        } 
                    />
                    <Route 
                        path="/reports" 
                        element={
                            <ProtectedRoute>
                                <Report />
                            </ProtectedRoute>
                        } 
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
