/**
 * Sales Order Form Component with Stock Validation
 */

import { useState, useEffect } from 'react';
import { salesService } from '../../services/modules/sales';
import { clientsService } from '../../services/modules/clients';
import { inventoryService } from '../../services/modules/inventory';
import Button from '../../components/Common/Button';
import Input from '../../components/Common/Input';
import Alert from '../../components/Common/Alert';
import toast from 'react-hot-toast';

const SalesOrderForm = ({ onClose }) => {
  const [formData, setFormData] = useState({
    client: '',
    order_number: '',
    order_date: new Date().toISOString().split('T')[0],
    expected_delivery_date: '',
    status: 'PENDING',
    warehouse: '',
    discount_amount: '',
    notes: '',
    sales_items: [],
  });
  const [clients, setClients] = useState([]);
  const [items, setItems] = useState([]);
  const [warehouses, setWarehouses] = useState([]);
  const [currentItem, setCurrentItem] = useState({
    item: '',
    quantity: '',
    unit_price: '',
    discount_percentage: '',
  });
  const [stockErrors, setStockErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadClients();
    loadItems();
    loadWarehouses();
  }, []);

  const loadClients = async () => {
    try {
      const response = await clientsService.getClients();
      setClients(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load clients');
    }
  };

  const loadItems = async () => {
    try {
      const response = await inventoryService.getItems();
      setItems(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load items');
    }
  };

  const loadWarehouses = async () => {
    try {
      const response = await inventoryService.getWarehouses();
      setWarehouses(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load warehouses');
    }
  };

  const checkStockAvailability = async (itemId, quantity, warehouseId) => {
    try {
      const stockResponse = await inventoryService.getStock({ item: itemId, warehouse: warehouseId });
      const stock = stockResponse.data.results || stockResponse.data;
      const stockEntry = stock.find(s => s.item === parseInt(itemId) && s.warehouse === parseInt(warehouseId));
      
      if (!stockEntry) {
        return { available: false, message: 'No stock found for this item in selected warehouse' };
      }
      
      if (stockEntry.available_quantity < quantity) {
        return {
          available: false,
          message: `Insufficient stock. Available: ${stockEntry.available_quantity}, Requested: ${quantity}`
        };
      }
      
      return { available: true };
    } catch (err) {
      return { available: false, message: 'Error checking stock availability' };
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleItemChange = async (e) => {
    const { name, value } = e.target;
    setCurrentItem(prev => ({ ...prev, [name]: value }));
    
    // Check stock when item or quantity changes
    if ((name === 'item' || name === 'quantity') && formData.warehouse && value) {
      const itemId = name === 'item' ? value : currentItem.item;
      const quantity = name === 'quantity' ? parseInt(value) : parseInt(currentItem.quantity);
      
      if (itemId && quantity && formData.warehouse) {
        const stockCheck = await checkStockAvailability(itemId, quantity, formData.warehouse);
        if (!stockCheck.available) {
          setStockErrors(prev => ({ ...prev, [itemId]: stockCheck.message }));
        } else {
          setStockErrors(prev => {
            const newErrors = { ...prev };
            delete newErrors[itemId];
            return newErrors;
          });
        }
      }
    }
  };

  const handleAddItem = async () => {
    if (!currentItem.item || !currentItem.quantity || !currentItem.unit_price) {
      toast.error('Please fill in item, quantity, and unit price');
      return;
    }

    if (!formData.warehouse) {
      toast.error('Please select a warehouse first');
      return;
    }

    // Check stock availability
    const stockCheck = await checkStockAvailability(
      currentItem.item,
      parseInt(currentItem.quantity),
      formData.warehouse
    );

    if (!stockCheck.available) {
      toast.error(stockCheck.message);
      setStockErrors(prev => ({ ...prev, [currentItem.item]: stockCheck.message }));
      return;
    }

    setFormData(prev => ({
      ...prev,
      sales_items: [...prev.sales_items, { ...currentItem }]
    }));

    setCurrentItem({
      item: '',
      quantity: '',
      unit_price: '',
      discount_percentage: '',
    });
    setStockErrors({});
  };

  const handleRemoveItem = (index) => {
    setFormData(prev => ({
      ...prev,
      sales_items: prev.sales_items.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.warehouse) {
      toast.error('Please select a warehouse');
      return;
    }
    
    if (formData.sales_items.length === 0) {
      toast.error('Please add at least one item');
      return;
    }

    // Final stock validation
    for (const item of formData.sales_items) {
      const stockCheck = await checkStockAvailability(
        item.item,
        parseInt(item.quantity),
        formData.warehouse
      );
      if (!stockCheck.available) {
        toast.error(`Insufficient stock for ${items.find(i => i.id === parseInt(item.item))?.name}: ${stockCheck.message}`);
        return;
      }
    }

    setLoading(true);

    try {
      await salesService.createSalesOrder(formData);
      toast.success('Sales order created successfully. Stock will be reserved automatically!');
      onClose();
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to create sales order';
      toast.error(errorMsg);
      if (errorMsg.includes('stock') || errorMsg.includes('Insufficient')) {
        // Show stock alert
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Client *</label>
          <select
            name="client"
            value={formData.client}
            onChange={handleChange}
            className="input-field"
            required
          >
            <option value="">Select Client</option>
            {clients.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
        <Input
          label="Order Number"
          name="order_number"
          value={formData.order_number}
          onChange={handleChange}
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Order Date"
          name="order_date"
          type="date"
          value={formData.order_date}
          onChange={handleChange}
          required
        />
        <Input
          label="Expected Delivery Date"
          name="expected_delivery_date"
          type="date"
          value={formData.expected_delivery_date}
          onChange={handleChange}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Warehouse *</label>
        <select
          name="warehouse"
          value={formData.warehouse}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="">Select Warehouse</option>
          {warehouses.map(w => (
            <option key={w.id} value={w.id}>{w.name}</option>
          ))}
        </select>
        <p className="text-xs text-gray-500 mt-1">Stock will be checked from this warehouse</p>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-4">Sales Items</h3>
        
        <div className="bg-gray-50 p-4 rounded-lg mb-4">
          <div className="grid grid-cols-12 gap-2 mb-2">
            <div className="col-span-4">
              <select
                name="item"
                value={currentItem.item}
                onChange={handleItemChange}
                className="input-field text-sm"
              >
                <option value="">Select Item</option>
                {items.map(i => (
                  <option key={i.id} value={i.id}>{i.name} ({i.sku})</option>
                ))}
              </select>
            </div>
            <Input
              label=""
              name="quantity"
              type="number"
              value={currentItem.quantity}
              onChange={handleItemChange}
              placeholder="Qty"
              className="col-span-2 text-sm"
            />
            <Input
              label=""
              name="unit_price"
              type="number"
              step="0.01"
              value={currentItem.unit_price}
              onChange={handleItemChange}
              placeholder="Unit Price"
              className="col-span-2 text-sm"
            />
            <Input
              label=""
              name="discount_percentage"
              type="number"
              step="0.01"
              value={currentItem.discount_percentage}
              onChange={handleItemChange}
              placeholder="Discount %"
              className="col-span-2 text-sm"
            />
            <Button type="button" onClick={handleAddItem} className="col-span-2">
              Add Item
            </Button>
          </div>
          {stockErrors[currentItem.item] && (
            <Alert type="error" message={stockErrors[currentItem.item]} />
          )}
        </div>

        <div className="space-y-2">
          {formData.sales_items.map((item, index) => {
            const itemData = items.find(i => i.id === parseInt(item.item));
            const hasError = stockErrors[item.item];
            return (
              <div key={index} className={`flex items-center justify-between bg-white p-3 rounded border ${hasError ? 'border-red-300' : ''}`}>
                <div className="flex-1">
                  <span className="font-medium">{itemData?.name || 'Item'}</span>
                  <span className="text-sm text-gray-500 ml-2">
                    Qty: {item.quantity} × ${item.unit_price}
                    {item.discount_percentage > 0 && ` (${item.discount_percentage}% off)`}
                  </span>
                  {hasError && (
                    <Alert type="error" message={hasError} />
                  )}
                </div>
                <button
                  type="button"
                  onClick={() => handleRemoveItem(index)}
                  className="text-red-600 hover:text-red-900 ml-4"
                >
                  Remove
                </button>
              </div>
            );
          })}
        </div>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <Button type="button" variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Create Order'}
        </Button>
      </div>
    </form>
  );
};

export default SalesOrderForm;

