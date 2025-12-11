/**
 * Sales Orders Page
 */

import { useState, useEffect } from 'react';
import { salesService } from '../../services/modules/sales';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import Modal from '../../components/common/Modal';
import SalesOrderForm from './SalesOrderForm';
import Alert from '../../components/common/Alert';
import { PlusIcon, TruckIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

const SalesOrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState(null);

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      setLoading(true);
      const response = await salesService.getSalesOrders();
      setOrders(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load sales orders');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingOrder(null);
    setIsModalOpen(true);
  };

  const handleMarkShipped = async (id) => {
    try {
      await salesService.markShipped(id);
      toast.success('Order marked as shipped. Stock reduced automatically!');
      loadOrders();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to mark order as shipped';
      toast.error(errorMsg);
      if (errorMsg.includes('stock') || errorMsg.includes('Insufficient')) {
        // Show alert for stock issues
      }
    }
  };

  const handleMarkDelivered = async (id) => {
    try {
      await salesService.markDelivered(id);
      toast.success('Order marked as delivered');
      loadOrders();
    } catch (err) {
      toast.error('Failed to mark order as delivered');
    }
  };

  const handleCancel = async (id) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;
    try {
      await salesService.cancelOrder(id);
      toast.success('Order cancelled. Reserved stock released.');
      loadOrders();
    } catch (err) {
      toast.error('Failed to cancel order');
    }
  };

  if (loading) return <Loading />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Sales Orders</h1>
        <Button onClick={handleCreate}>
          <PlusIcon className="h-5 w-5 inline mr-2" />
          Create Sales Order
        </Button>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order Number</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Client</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Items</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{order.order_number}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{order.client_name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {format(new Date(order.order_date), 'MMM dd, yyyy')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                    ${order.total_amount}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      order.status === 'DELIVERED' ? 'bg-green-100 text-green-800' :
                      order.status === 'SHIPPED' ? 'bg-blue-100 text-blue-800' :
                      order.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                      order.status === 'CANCELLED' ? 'bg-red-100 text-red-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{order.item_count || 0}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    {order.status === 'PENDING' && (
                      <>
                        <Button
                          variant="success"
                          onClick={() => handleMarkShipped(order.id)}
                          className="text-xs"
                        >
                          <TruckIcon className="h-4 w-4 inline mr-1" />
                          Ship
                        </Button>
                        <Button
                          variant="danger"
                          onClick={() => handleCancel(order.id)}
                          className="text-xs"
                        >
                          <XCircleIcon className="h-4 w-4 inline mr-1" />
                          Cancel
                        </Button>
                      </>
                    )}
                    {order.status === 'SHIPPED' && (
                      <Button
                        variant="success"
                        onClick={() => handleMarkDelivered(order.id)}
                        className="text-xs"
                      >
                        <CheckCircleIcon className="h-4 w-4 inline mr-1" />
                        Deliver
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Sales Order" size="lg">
        <SalesOrderForm onClose={() => { setIsModalOpen(false); loadOrders(); }} />
      </Modal>
    </div>
  );
};

export default SalesOrdersPage;

