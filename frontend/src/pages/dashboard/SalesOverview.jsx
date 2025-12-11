/**
 * Sales Overview Component with Charts
 */

import { useMemo } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { format, subDays } from 'date-fns';
import { BanknotesIcon } from '@heroicons/react/24/outline';

const SalesOverview = ({ data }) => {
  const orders = data.orders || [];

  const statusData = useMemo(() => {
    const statusCounts = {
      PENDING: 0,
      CONFIRMED: 0,
      SHIPPED: 0,
      DELIVERED: 0,
      CANCELLED: 0,
    };

    orders.forEach(order => {
      statusCounts[order.status] = (statusCounts[order.status] || 0) + 1;
    });

    return Object.entries(statusCounts).map(([name, value]) => ({ name, value }));
  }, [orders]);

  const revenueData = useMemo(() => {
    const last7Days = Array.from({ length: 7 }, (_, i) => {
      const date = subDays(new Date(), 6 - i);
      return {
        date: format(date, 'MMM dd'),
        revenue: 0,
      };
    });

    orders.forEach(order => {
      if (order.status === 'SHIPPED' || order.status === 'DELIVERED') {
        const orderDate = new Date(order.order_date);
        const dayIndex = Math.floor((new Date() - orderDate) / (1000 * 60 * 60 * 24));
        if (dayIndex >= 0 && dayIndex < 7) {
          last7Days[dayIndex].revenue += parseFloat(order.total_amount || 0);
        }
      }
    });

    return last7Days;
  }, [orders]);

  const totalRevenue = useMemo(() => {
    return orders
      .filter(o => o.status === 'SHIPPED' || o.status === 'DELIVERED')
      .reduce((sum, o) => sum + parseFloat(o.total_amount || 0), 0);
  }, [orders]);

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6b7280'];

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Sales Overview</h2>
        <BanknotesIcon className="h-6 w-6 text-green-600" />
      </div>

      <div className="mb-6">
        <div className="bg-green-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Revenue</p>
          <p className="text-2xl font-bold text-green-600">${totalRevenue.toFixed(2)}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
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

      <div className="h-48">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">Revenue Trend (Last 7 Days)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={2} name="Revenue ($)" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default SalesOverview;

