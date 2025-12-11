/**
 * Main Inventory Page with Tabs
 */

import { useState } from 'react';
import ItemsList from './ItemsList';
import StockView from './StockView';

const InventoryPage = () => {
  const [activeTab, setActiveTab] = useState('items');

  const tabs = [
    { id: 'items', label: 'Items' },
    { id: 'stock', label: 'Stock Levels' },
  ];

  return (
    <div>
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === 'items' && <ItemsList />}
      {activeTab === 'stock' && <StockView />}
    </div>
  );
};

export default InventoryPage;

