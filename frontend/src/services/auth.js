/**
 * Authentication Service
 */

import axios from 'axios';
import api from './api';

export const authService = {
  login: async (username, password) => {
    const response = await axios.post('http://localhost:8000/api/token/', { username, password });
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    return { access, refresh };
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },

  getToken: () => {
    return localStorage.getItem('access_token');
  },
};

