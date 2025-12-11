/**
 * Inventory Overview Component with Charts
 */

import { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { inventoryService } from '../../services/modules/inventory';
import { useState, useEffect } from 'react';
import { CubeIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

const InventoryOverview = ({ data }) => {
  const [stockValue, setStockValue] = useState(0);
  const [lowStockCount, setLowStockCount] = useState(0);

  useEffect(() => {
    loadStockData();
  }, []);

  const loadStockData = async () => {
    try {
      const [stockResponse, lowStockResponse] = await Promise.all([
        inventoryService.getStock(),
        inventoryService.getLowStock(),
      ]);

      const stock = stockResponse.data.results || stockResponse.data || [];
      const lowStock = lowStockResponse.data.results || lowStockResponse.data || [];

      // Calculate total stock value
      const totalValue = stock.reduce((sum, s) => {
        return sum + (s.quantity * (s.average_cost || 0));
      }, 0);

      setStockValue(totalValue);
      setLowStockCount(lowStock.length);
    } catch (err) {
      console.error('Failed to load stock data');
    }
  };

  const chartData = useMemo(() => {
    if (!data.lowStockItems || data.lowStockItems.length === 0) {
      return [];
    }

    return data.lowStockItems.slice(0, 10).map(item => ({
      name: item.name?.substring(0, 15) || 'Item',
      stock: item.total_stock || 0,
      reorder: item.reorder_level || 0,
    }));
  }, [data.lowStockItems]);

  const COLORS = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981'];

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Inventory Overview</h2>
        <CubeIcon className="h-6 w-6 text-primary-600" />
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <p className="text-sm text-gray-600">Total Stock Value</p>
          <p className="text-2xl font-bold text-blue-600">${stockValue.toFixed(2)}</p>
        </div>
        <div className="bg-red-50 p-4 rounded-lg">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-600 mr-2" />
            <div>
              <p className="text-sm text-gray-600">Low Stock Items</p>
              <p className="text-2xl font-bold text-red-600">{lowStockCount}</p>
            </div>
          </div>
        </div>
      </div>

      {chartData.length > 0 ? (
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="stock" fill="#3b82f6" name="Current Stock" />
              <Bar dataKey="reorder" fill="#ef4444" name="Reorder Level" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <p>No low stock items</p>
        </div>
      )}
    </div>
  );
};

export default InventoryOverview;

