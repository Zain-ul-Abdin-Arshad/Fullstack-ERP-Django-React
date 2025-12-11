/**
 * Financial Overview Component with Charts
 */

import { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { accountsService } from '../../services/modules/accounts';
import { useState, useEffect } from 'react';
import { ChartBarIcon } from '@heroicons/react/24/outline';

const FinancialOverview = ({ data }) => {
  const [profitLoss, setProfitLoss] = useState(data || {});

  useEffect(() => {
    loadProfitLoss();
  }, []);

  const loadProfitLoss = async () => {
    try {
      const startDate = new Date(new Date().setDate(1)).toISOString().split('T')[0];
      const endDate = new Date().toISOString().split('T')[0];
      const response = await accountsService.calculateProfitLoss({
        start_date: startDate,
        end_date: endDate,
      });
      setProfitLoss(response.data);
    } catch (err) {
      console.error('Failed to load profit/loss data');
    }
  };

  const chartData = useMemo(() => {
    if (!profitLoss.total_revenue) return [];
    
    return [
      { name: 'Revenue', value: profitLoss.total_revenue || 0 },
      { name: 'COGS', value: profitLoss.total_cost_of_goods_sold || 0 },
      { name: 'Expenses', value: profitLoss.total_expenses || 0 },
      { name: 'Gross Profit', value: profitLoss.gross_profit || 0 },
      { name: 'Net Profit', value: profitLoss.net_profit || 0 },
    ];
  }, [profitLoss]);

  const profitMargin = useMemo(() => {
    if (!profitLoss.total_revenue || profitLoss.total_revenue === 0) return 0;
    return ((profitLoss.net_profit || 0) / profitLoss.total_revenue) * 100;
  }, [profitLoss]);

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Financial Overview</h2>
        <ChartBarIcon className="h-6 w-6 text-purple-600" />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className={`p-4 rounded-lg ${profitLoss.net_profit >= 0 ? 'bg-green-50' : 'bg-red-50'}`}>
          <p className="text-sm text-gray-600">Net Profit</p>
          <p className={`text-2xl font-bold ${profitLoss.net_profit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${(profitLoss.net_profit || 0).toFixed(2)}
          </p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Profit Margin</p>
          <p className="text-2xl font-bold text-purple-600">{profitMargin.toFixed(2)}%</p>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
            <YAxis />
            <Tooltip formatter={(value) => `$${value.toFixed(2)}`} />
            <Legend />
            <Bar dataKey="value" fill="#8b5cf6" name="Amount ($)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div>
          <p className="text-gray-600">Revenue:</p>
          <p className="font-semibold">${(profitLoss.total_revenue || 0).toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-600">COGS:</p>
          <p className="font-semibold">${(profitLoss.total_cost_of_goods_sold || 0).toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-600">Gross Profit:</p>
          <p className="font-semibold text-green-600">${(profitLoss.gross_profit || 0).toFixed(2)}</p>
        </div>
        <div>
          <p className="text-gray-600">Expenses:</p>
          <p className="font-semibold">${(profitLoss.total_expenses || 0).toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};

export default FinancialOverview;

