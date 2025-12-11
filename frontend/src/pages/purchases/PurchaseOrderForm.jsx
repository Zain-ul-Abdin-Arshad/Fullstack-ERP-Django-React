/**
 * Purchase Order Form Component
 */

import { useState, useEffect } from 'react';
import { purchasesService } from '../../services/modules/purchases';
import { vendorsService } from '../../services/modules/vendors';
import { inventoryService } from '../../services/modules/inventory';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import toast from 'react-hot-toast';

const PurchaseOrderForm = ({ onClose }) => {
  const [formData, setFormData] = useState({
    vendor: '',
    order_number: '',
    order_date: new Date().toISOString().split('T')[0],
    expected_delivery_date: '',
    status: 'PENDING',
    notes: '',
    purchase_items: [],
  });
  const [vendors, setVendors] = useState([]);
  const [items, setItems] = useState([]);
  const [currentItem, setCurrentItem] = useState({
    item: '',
    quantity: '',
    unit_cost: '',
    freight_cost: '',
    customs_duty: '',
    other_costs: '',
    received_quantity: '',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadVendors();
    loadItems();
  }, []);

  const loadVendors = async () => {
    try {
      const response = await vendorsService.getVendors();
      setVendors(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load vendors');
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleItemChange = (e) => {
    const { name, value } = e.target;
    setCurrentItem(prev => ({ ...prev, [name]: value }));
  };

  const handleAddItem = () => {
    if (!currentItem.item || !currentItem.quantity || !currentItem.unit_cost) {
      toast.error('Please fill in item, quantity, and unit cost');
      return;
    }

    setFormData(prev => ({
      ...prev,
      purchase_items: [...prev.purchase_items, { ...currentItem, received_quantity: currentItem.quantity }]
    }));

    setCurrentItem({
      item: '',
      quantity: '',
      unit_cost: '',
      freight_cost: '',
      customs_duty: '',
      other_costs: '',
      received_quantity: '',
    });
  };

  const handleRemoveItem = (index) => {
    setFormData(prev => ({
      ...prev,
      purchase_items: prev.purchase_items.filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.purchase_items.length === 0) {
      toast.error('Please add at least one item');
      return;
    }

    setLoading(true);

    try {
      await purchasesService.createPurchaseOrder(formData);
      toast.success('Purchase order created successfully');
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create purchase order');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Vendor *</label>
          <select
            name="vendor"
            value={formData.vendor}
            onChange={handleChange}
            className="input-field"
            required
          >
            <option value="">Select Vendor</option>
            {vendors.map(v => (
              <option key={v.id} value={v.id}>{v.name}</option>
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
        <h3 className="text-lg font-semibold mb-4">Purchase Items</h3>
        
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
              name="unit_cost"
              type="number"
              step="0.01"
              value={currentItem.unit_cost}
              onChange={handleItemChange}
              placeholder="Unit Cost"
              className="col-span-2 text-sm"
            />
            <Input
              label=""
              name="freight_cost"
              type="number"
              step="0.01"
              value={currentItem.freight_cost}
              onChange={handleItemChange}
              placeholder="Freight"
              className="col-span-2 text-sm"
            />
            <Input
              label=""
              name="customs_duty"
              type="number"
              step="0.01"
              value={currentItem.customs_duty}
              onChange={handleItemChange}
              placeholder="Duty"
              className="col-span-2 text-sm"
            />
            <Button type="button" onClick={handleAddItem} className="col-span-2">
              Add Item
            </Button>
          </div>
        </div>

        <div className="space-y-2">
          {formData.purchase_items.map((item, index) => {
            const itemData = items.find(i => i.id === parseInt(item.item));
            return (
              <div key={index} className="flex items-center justify-between bg-white p-3 rounded border">
                <div className="flex-1">
                  <span className="font-medium">{itemData?.name || 'Item'}</span>
                  <span className="text-sm text-gray-500 ml-2">
                    Qty: {item.quantity} × ${item.unit_cost}
                    {item.freight_cost > 0 && ` + Freight: $${item.freight_cost}`}
                    {item.customs_duty > 0 && ` + Duty: $${item.customs_duty}`}
                  </span>
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

export default PurchaseOrderForm;

