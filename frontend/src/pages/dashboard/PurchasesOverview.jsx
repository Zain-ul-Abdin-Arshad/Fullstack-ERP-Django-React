/**
 * Purchases Overview Component with Charts
 */

import { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { ShoppingCartIcon } from '@heroicons/react/24/outline';

const PurchasesOverview = ({ data }) => {
  const orders = data.orders || [];

  const statusData = useMemo(() => {
    const statusCounts = {
      PENDING: 0,
      RECEIVED: 0,
      PARTIAL: 0,
      CANCELLED: 0,
    };

    orders.forEach(order => {
      statusCounts[order.status] = (statusCounts[order.status] || 0) + 1;
    });

    return Object.entries(statusCounts).map(([name, value]) => ({ name, value }));
  }, [orders]);

  const totalSpent = useMemo(() => {
    return orders
      .filter(o => o.status === 'RECEIVED')
      .reduce((sum, o) => sum + parseFloat(o.total_amount || 0), 0);
  }, [orders]);

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'];

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Purchases Overview</h2>
        <ShoppingCartIcon className="h-6 w-6 text-blue-600" />
      </div>

      <div className="mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Spent (Received Orders)</p>
          <p className="text-2xl font-bold text-blue-600">${totalSpent.toFixed(2)}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={statusData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={60}
                fill="#8884d8"
                dataKey="value"
              >
                {statusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={statusData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default PurchasesOverview;

