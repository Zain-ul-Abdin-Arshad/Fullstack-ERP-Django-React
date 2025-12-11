/**
 * Vendor Form Component
 */

import { useState, useEffect } from 'react';
import { vendorsService } from '../../services/modules/vendors';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import toast from 'react-hot-toast';

const VendorForm = ({ vendor, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    country: '',
    contact_number: '',
    email: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    website: '',
    tax_id: '',
    payment_terms: '',
    credit_limit: '',
    is_active: true,
    notes: '',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (vendor) {
      setFormData({
        name: vendor.name || '',
        code: vendor.code || '',
        country: vendor.country || '',
        contact_number: vendor.contact_number || '',
        email: vendor.email || '',
        address: vendor.address || '',
        city: vendor.city || '',
        state: vendor.state || '',
        postal_code: vendor.postal_code || '',
        website: vendor.website || '',
        tax_id: vendor.tax_id || '',
        payment_terms: vendor.payment_terms || '',
        credit_limit: vendor.credit_limit || '',
        is_active: vendor.is_active !== undefined ? vendor.is_active : true,
        notes: vendor.notes || '',
      });
    }
  }, [vendor]);

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
      if (vendor) {
        await vendorsService.updateVendor(vendor.id, formData);
        toast.success('Vendor updated successfully');
      } else {
        await vendorsService.createVendor(formData);
        toast.success('Vendor created successfully');
      }
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save vendor');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Name"
        name="name"
        value={formData.name}
        onChange={handleChange}
        required
      />

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Code"
          name="code"
          value={formData.code}
          onChange={handleChange}
        />
        <Input
          label="Country"
          name="country"
          value={formData.country}
          onChange={handleChange}
          required
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Contact Number"
          name="contact_number"
          value={formData.contact_number}
          onChange={handleChange}
          required
        />
        <Input
          label="Email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>

      <Input
        label="Address"
        name="address"
        value={formData.address}
        onChange={handleChange}
      />

      <div className="grid grid-cols-3 gap-4">
        <Input
          label="City"
          name="city"
          value={formData.city}
          onChange={handleChange}
        />
        <Input
          label="State"
          name="state"
          value={formData.state}
          onChange={handleChange}
        />
        <Input
          label="Postal Code"
          name="postal_code"
          value={formData.postal_code}
          onChange={handleChange}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Website"
          name="website"
          type="url"
          value={formData.website}
          onChange={handleChange}
        />
        <Input
          label="Tax ID"
          name="tax_id"
          value={formData.tax_id}
          onChange={handleChange}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Payment Terms"
          name="payment_terms"
          value={formData.payment_terms}
          onChange={handleChange}
          placeholder="e.g., Net 30"
        />
        <Input
          label="Credit Limit"
          name="credit_limit"
          type="number"
          step="0.01"
          value={formData.credit_limit}
          onChange={handleChange}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Notes</label>
        <textarea
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          rows={3}
          className="input-field"
        />
      </div>

      <div className="flex items-center">
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
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <Button type="button" variant="secondary" onClick={onClose}>
          Cancel
        </Button>
        <Button type="submit" disabled={loading}>
          {loading ? 'Saving...' : vendor ? 'Update' : 'Create'}
        </Button>
      </div>
    </form>
  );
};

export default VendorForm;

