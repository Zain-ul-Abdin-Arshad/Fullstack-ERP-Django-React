/**
 * Stock View Page - View stock per warehouse
 */

import { useState, useEffect } from 'react';
import { inventoryService } from '../../services/modules/inventory';
import Loading from '../../components/Common/Loading';
import Alert from '../../components/Common/Alert';
import { BuildingStorefrontIcon } from '@heroicons/react/24/outline';

const StockView = () => {
  const [stock, setStock] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [selectedWarehouse, setSelectedWarehouse] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadWarehouses();
  }, []);

  useEffect(() => {
    if (selectedWarehouse) {
      loadStock();
    } else {
      loadAllStock();
    }
  }, [selectedWarehouse]);

  const loadWarehouses = async () => {
    try {
      const response = await inventoryService.getWarehouses();
      setWarehouses(response.data.results || response.data);
    } catch (err) {
      setError('Failed to load warehouses');
    }
  };

  const loadStock = async () => {
    try {
      setLoading(true);
      const response = await inventoryService.getStock({ warehouse: selectedWarehouse });
      setStock(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load stock');
    } finally {
      setLoading(false);
    }
  };

  const loadAllStock = async () => {
    try {
      setLoading(true);
      const response = await inventoryService.getStock();
      setStock(response.data.results || response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load stock');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Stock Levels</h1>
        <div className="flex items-center space-x-4">
          <select
            value={selectedWarehouse}
            onChange={(e) => setSelectedWarehouse(e.target.value)}
            className="input-field max-w-xs"
          >
            <option value="">All Warehouses</option>
            {warehouses.map(wh => (
              <option key={wh.id} value={wh.id}>{wh.name}</option>
            ))}
          </select>
        </div>
      </div>

      {error && <Alert type="error" message={error} />}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stock.map((stockItem) => (
          <div key={stockItem.id} className="card">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{stockItem.item_name}</h3>
                <p className="text-sm text-gray-500 mt-1">{stockItem.item_sku}</p>
                <div className="mt-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <BuildingStorefrontIcon className="h-4 w-4 mr-2" />
                    {stockItem.warehouse_name}
                  </div>
                </div>
              </div>
            </div>
            <div className="mt-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Quantity:</span>
                <span className={`text-sm font-semibold ${stockItem.is_low_stock ? 'text-red-600' : 'text-gray-900'}`}>
                  {stockItem.quantity}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Available:</span>
                <span className="text-sm font-semibold text-gray-900">{stockItem.available_quantity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Reserved:</span>
                <span className="text-sm font-semibold text-gray-900">{stockItem.reserved_quantity}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Min Level:</span>
                <span className="text-sm font-semibold text-gray-900">{stockItem.min_quantity}</span>
              </div>
              {stockItem.is_low_stock && (
                <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
                  <p className="text-xs text-red-800 font-semibold">Low Stock Alert!</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {stock.length === 0 && (
        <div className="card text-center py-12">
          <p className="text-gray-500">No stock data available</p>
        </div>
      )}
    </div>
  );
};

export default StockView;

