/**
 * Item Form Component
 */

import { useState, useEffect } from 'react';
import { inventoryService } from '../../services/modules/inventory';
import Button from '../../components/Common/Button';
import Input from '../../components/Common/Input';
import toast from 'react-hot-toast';

const ItemForm = ({ item, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    sku: '',
    barcode: '',
    description: '',
    category: '',
    vendor: '',
    cost_price: '',
    selling_price: '',
    unit: 'PCS',
    reorder_level: 0,
    reorder_quantity: 0,
    is_active: true,
    is_trackable: true,
    allow_backorder: false,
  });
  const [categories, setCategories] = useState([]);
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadCategories();
    loadVendors();
    if (item) {
      setFormData({
        name: item.name || '',
        sku: item.sku || '',
        barcode: item.barcode || '',
        description: item.description || '',
        category: item.category || '',
        vendor: item.vendor || '',
        cost_price: item.cost_price || '',
        selling_price: item.selling_price || '',
        unit: item.unit || 'PCS',
        reorder_level: item.reorder_level || 0,
        reorder_quantity: item.reorder_quantity || 0,
        is_active: item.is_active !== undefined ? item.is_active : true,
        is_trackable: item.is_trackable !== undefined ? item.is_trackable : true,
        allow_backorder: item.allow_backorder || false,
      });
    }
  }, [item]);

  const loadCategories = async () => {
    try {
      const response = await inventoryService.getCategories();
      setCategories(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load categories');
    }
  };

  const loadVendors = async () => {
    try {
      const response = await inventoryService.getVendors();
      setVendors(response.data.results || response.data);
    } catch (err) {
      // Vendors service might not exist yet
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (item) {
        await inventoryService.updateItem(item.id, formData);
        toast.success('Item updated successfully');
      } else {
        await inventoryService.createItem(formData);
        toast.success('Item created successfully');
      }
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save item');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <Input
          label="SKU"
          name="sku"
          value={formData.sku}
          onChange={handleChange}
          required
        />
      </div>

      <Input
        label="Barcode"
        name="barcode"
        value={formData.barcode}
        onChange={handleChange}
      />

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
        <select
          name="category"
          value={formData.category}
          onChange={handleChange}
          className="input-field"
          required
        >
          <option value="">Select Category</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Cost Price"
          name="cost_price"
          type="number"
          step="0.01"
          value={formData.cost_price}
          onChange={handleChange}
          required
        />
        <Input
          label="Selling Price"
          name="selling_price"
          type="number"
          step="0.01"
          value={formData.selling_price}
          onChange={handleChange}
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Reorder Level"
          name="reorder_level"
          type="number"
          value={formData.reorder_level}
          onChange={handleChange}
        />
        <Input
          label="Reorder Quantity"
          name="reorder_quantity"
          type="number"
          value={formData.reorder_quantity}
          onChange={handleChange}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Unit</label>
        <select
          name="unit"
          value={formData.unit}
          onChange={handleChange}
          className="input-field"
        >
          <option value="PCS">Pieces</option>
          <option value="BOX">Box</option>
          <option value="PKG">Package</option>
          <option value="SET">Set</option>
          <option value="PAIR">Pair</option>
          <option value="KG">Kilogram</option>
          <option value="L">Liter</option>
          <option value="M">Meter</option>
        </select>
      </div>

      <div className="flex items-center space-x-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            name="is_active"
            checked={formData.is_active}
            onChange={handleChange}
            className="mr-2"
          />
          <span className="text-sm text-gray-700">Active</span>
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            name="is_trackable"
            checked={formData.is_trackable}
            onChange={handleChange}
            className="mr-2"
          />
          <span className="text-sm text-gray-700">Trackable</span>
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            name="allow_backorder"
            checked={formData.allow_backorder}
            onChange={handleChange}
            className="mr-2"
          />
          <span className="text-sm text-gray-700">Allow Backorder</span>
        </label>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <Button type="button" variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? 'Saving...' : item ? 'Update' : 'Create'}
        </Button>
      </div>
    </form>
  );
};

export default ItemForm;

