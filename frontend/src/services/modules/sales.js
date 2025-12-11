/**
 * Sales API Service
 */

import api from '../api';

export const salesService = {
  // Sales Orders
  getSalesOrders: (params) => api.get('/sales/orders/', { params }),
  getSalesOrder: (id) => api.get(`/sales/orders/${id}/`),
  createSalesOrder: (data) => api.post('/sales/orders/', data),
  updateSalesOrder: (id, data) => api.put(`/sales/orders/${id}/`, data),
  deleteSalesOrder: (id) => api.delete(`/sales/orders/${id}/`),
  markShipped: (id) => api.post(`/sales/orders/${id}/mark_shipped/`),
  markDelivered: (id) => api.post(`/sales/orders/${id}/mark_delivered/`),
  cancelOrder: (id) => api.post(`/sales/orders/${id}/cancel/`),
  recalculateTotal: (id) => api.post(`/sales/orders/${id}/recalculate_total/`),

  // Sales Items
  getSalesItems: (params) => api.get('/sales/items/', { params }),
  getSalesItem: (id) => api.get(`/sales/items/${id}/`),
  createSalesItem: (data) => api.post('/sales/items/', data),
  updateSalesItem: (id, data) => api.put(`/sales/items/${id}/`, data),
  deleteSalesItem: (id) => api.delete(`/sales/items/${id}/`),
};
