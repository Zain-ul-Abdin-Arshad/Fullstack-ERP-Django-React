/**
 * Inventory API Service
 */

import api from '../api';

export const inventoryService = {
  // Categories
  getCategories: () => api.get('/inventory/categories/'),
  getCategory: (id) => api.get(`/inventory/categories/${id}/`),
  createCategory: (data) => api.post('/inventory/categories/', data),
  updateCategory: (id, data) => api.put(`/inventory/categories/${id}/`, data),
  deleteCategory: (id) => api.delete(`/inventory/categories/${id}/`),

  // Warehouses
  getWarehouses: () => api.get('/inventory/warehouses/'),
  getWarehouse: (id) => api.get(`/inventory/warehouses/${id}/`),
  createWarehouse: (data) => api.post('/inventory/warehouses/', data),
  updateWarehouse: (id, data) => api.put(`/inventory/warehouses/${id}/`, data),
  deleteWarehouse: (id) => api.delete(`/inventory/warehouses/${id}/`),

  // Items
  getItems: (params) => api.get('/inventory/items/', { params }),
  getItem: (id) => api.get(`/inventory/items/${id}/`),
  createItem: (data) => api.post('/inventory/items/', data),
  updateItem: (id, data) => api.put(`/inventory/items/${id}/`, data),
  deleteItem: (id) => api.delete(`/inventory/items/${id}/`),
  getItemStock: (id) => api.get(`/inventory/items/${id}/stock/`),
  getLowStockItems: () => api.get('/inventory/items/low_stock/'),

  // Stock
  getStock: (params) => api.get('/inventory/stock/', { params }),
  getStockEntry: (id) => api.get(`/inventory/stock/${id}/`),
  createStock: (data) => api.post('/inventory/stock/', data),
  updateStock: (id, data) => api.put(`/inventory/stock/${id}/`, data),
  deleteStock: (id) => api.delete(`/inventory/stock/${id}/`),
  getLowStock: () => api.get('/inventory/stock/low_stock/'),
  getOutOfStock: () => api.get('/inventory/stock/out_of_stock/'),
};

