/**
 * Purchases API Service
 */

import api from '../api';

export const purchasesService = {
  // Purchase Orders
  getPurchaseOrders: (params) => api.get('/purchases/orders/', { params }),
  getPurchaseOrder: (id) => api.get(`/purchases/orders/${id}/`),
  createPurchaseOrder: (data) => api.post('/purchases/orders/', data),
  updatePurchaseOrder: (id, data) => api.put(`/purchases/orders/${id}/`, data),
  deletePurchaseOrder: (id) => api.delete(`/purchases/orders/${id}/`),
  markReceived: (id) => api.post(`/purchases/orders/${id}/mark_received/`),
  recalculateTotal: (id) => api.post(`/purchases/orders/${id}/recalculate_total/`),

  // Purchase Items
  getPurchaseItems: (params) => api.get('/purchases/items/', { params }),
  getPurchaseItem: (id) => api.get(`/purchases/items/${id}/`),
  createPurchaseItem: (data) => api.post('/purchases/items/', data),
  updatePurchaseItem: (id, data) => api.put(`/purchases/items/${id}/`, data),
  deletePurchaseItem: (id) => api.delete(`/purchases/items/${id}/`),
};
