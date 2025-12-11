/**
 * Client Form Component
 */

import { useState, useEffect } from 'react';
import { clientsService } from '../../services/modules/clients';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import toast from 'react-hot-toast';

const ClientForm = ({ client, onClose }) => {
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    country: '',
    city: '',
    contact_number: '',
    email: '',
    address: '',
    state: '',
    postal_code: '',
    website: '',
    tax_id: '',
    payment_terms: '',
    credit_limit: '',
    discount_percentage: 0,
    client_type: 'RETAILER',
    is_active: true,
    notes: '',
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (client) {
      setFormData({
        name: client.name || '',
        code: client.code || '',
        country: client.country || '',
        city: client.city || '',
        contact_number: client.contact_number || '',
        email: client.email || '',
        address: client.address || '',
        state: client.state || '',
        postal_code: client.postal_code || '',
        website: client.website || '',
        tax_id: client.tax_id || '',
        payment_terms: client.payment_terms || '',
        credit_limit: client.credit_limit || '',
        discount_percentage: client.discount_percentage || 0,
        client_type: client.client_type || 'RETAILER',
        is_active: client.is_active !== undefined ? client.is_active : true,
        notes: client.notes || '',
      });
    }
  }, [client]);

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
      if (client) {
        await clientsService.updateClient(client.id, formData);
        toast.success('Client updated successfully');
      } else {
        await clientsService.createClient(formData);
        toast.success('Client created successfully');
      }
      onClose();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save client');
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
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Client Type</label>
          <select
            name="client_type"
            value={formData.client_type}
            onChange={handleChange}
            className="input-field"
          >
            <option value="INDIVIDUAL">Individual</option>
            <option value="RETAILER">Retailer</option>
            <option value="WHOLESALER">Wholesaler</option>
            <option value="DISTRIBUTOR">Distributor</option>
            <option value="DEALER">Dealer</option>
            <option value="OTHER">Other</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Country"
          name="country"
          value={formData.country}
          onChange={handleChange}
          required
        />
        <Input
          label="City"
          name="city"
          value={formData.city}
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
        <Input
          label="Discount %"
          name="discount_percentage"
          type="number"
          step="0.01"
          value={formData.discount_percentage}
          onChange={handleChange}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <Input
          label="Payment Terms"
          name="payment_terms"
          value={formData.payment_terms}
          onChange={handleChange}
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
          {loading ? 'Saving...' : client ? 'Update' : 'Create'}
        </Button>
      </div>
    </form>
  );
};

export default ClientForm;

