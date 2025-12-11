/**
 * Clients API Service
 */

import api from '../api';

export const clientsService = {
  getClients: (params) => api.get('/clients/', { params }),
  getClient: (id) => api.get(`/clients/${id}/`),
  createClient: (data) => api.post('/clients/', data),
  updateClient: (id, data) => api.put(`/clients/${id}/`, data),
  deleteClient: (id) => api.delete(`/clients/${id}/`),
};

