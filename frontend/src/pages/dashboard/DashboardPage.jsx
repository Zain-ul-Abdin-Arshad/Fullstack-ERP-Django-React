/**
 * Dashboard Page with Charts
 */

import { useState, useEffect } from 'react';
import { inventoryService } from '../../services/modules/inventory';
import { salesService } from '../../services/modules/sales';
import { purchasesService } from '../../services/modules/purchases';
import { accountsService } from '../../services/modules/accounts';
import Loading from '../../components/common/Loading';
import InventoryOverview from './InventoryOverview';
import SalesOverview from './SalesOverview';
import PurchasesOverview from './PurchasesOverview';
import FinancialOverview from './FinancialOverview';

const DashboardPage = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    inventory: {},
    sales: {},
    purchases: {},
    financial: {},
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      // Load all dashboard data in parallel
      const [lowStock, salesOrders, purchaseOrders, profitLoss] = await Promise.all([
        inventoryService.getLowStock().catch(() => ({ data: [] })),
        salesService.getSalesOrders().catch(() => ({ data: { results: [] } })),
        purchasesService.getPurchaseOrders().catch(() => ({ data: { results: [] } })),
        accountsService.calculateProfitLoss({
          start_date: new Date(new Date().setDate(1)).toISOString().split('T')[0],
          end_date: new Date().toISOString().split('T')[0],
        }).catch(() => ({ data: {} })),
      ]);

      setStats({
        inventory: {
          lowStockItems: lowStock.data.results || lowStock.data || [],
        },
        sales: {
          orders: salesOrders.data.results || salesOrders.data || [],
        },
        purchases: {
          orders: purchaseOrders.data.results || purchaseOrders.data || [],
        },
        financial: profitLoss.data || {},
      });
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <button
          onClick={loadDashboardData}
          className="px-4 py-2 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
        >
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InventoryOverview data={stats.inventory} />
        <SalesOverview data={stats.sales} />
        <PurchasesOverview data={stats.purchases} />
        <FinancialOverview data={stats.financial} />
      </div>
    </div>
  );
};

export default DashboardPage;

