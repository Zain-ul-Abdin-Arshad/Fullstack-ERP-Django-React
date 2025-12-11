/**
 * Accounts API Service
 */

import api from '../api';

export const accountsService = {
  // Payments
  getPayments: (params) => api.get('/accounts/payments/', { params }),
  getPayment: (id) => api.get(`/accounts/payments/${id}/`),
  createPayment: (data) => api.post('/accounts/payments/', data),
  updatePayment: (id, data) => api.put(`/accounts/payments/${id}/`, data),
  deletePayment: (id) => api.delete(`/accounts/payments/${id}/`),
  reconcilePayment: (id) => api.post(`/accounts/payments/${id}/reconcile/`),

  // Ledger
  getLedgerEntries: (params) => api.get('/accounts/ledger/', { params }),
  getLedgerEntry: (id) => api.get(`/accounts/ledger/${id}/`),
  getLedgerSummary: (params) => api.get('/accounts/ledger/summary/', { params }),

  // Profit/Loss
  getProfitLossReports: (params) => api.get('/accounts/profit-loss/', { params }),
  getProfitLossReport: (id) => api.get(`/accounts/profit-loss/${id}/`),
  calculateProfitLoss: (data) => api.post('/accounts/profit-loss/calculate/', data),
  createProfitLossReport: (data) => api.post('/accounts/profit-loss/create_report/', data),
};
