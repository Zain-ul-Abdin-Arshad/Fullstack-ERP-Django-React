/**
 * Vendors Page with CRUD operations
 */

import { useState, useEffect } from 'react';
import { vendorsService } from '../../services/modules/vendors';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import Modal from '../../components/common/Modal';
import VendorForm from './VendorForm';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const VendorsPage = () => {
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingVendor, setEditingVendor] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadVendors();
  }, []);

  const loadVendors = async () => {
    try {
      setLoading(true);
      const response = await vendorsService.getVendors({ search: searchTerm });
      setVendors(response.data.results || response.data);
    } catch (err) {
      toast.error('Failed to load vendors');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setEditingVendor(null);
    setIsModalOpen(true);
  };

  const handleEdit = (vendor) => {
    setEditingVendor(vendor);
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this vendor?')) return;
    try {
      await vendorsService.deleteVendor(id);
      toast.success('Vendor deleted successfully');
      loadVendors();
    } catch (err) {
      toast.error('Failed to delete vendor');
    }
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
    setEditingVendor(null);
    loadVendors();
  };

  if (loading) return <Loading />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Vendors</h1>
        <Button onClick={handleCreate}>
          <PlusIcon className="h-5 w-5 inline mr-2" />
          Add Vendor
        </Button>
      </div>

      <div className="mb-4">
        <input
          type="text"
          placeholder="Search vendors..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && loadVendors()}
          className="input-field max-w-md"
        />
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Country</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {vendors.map((vendor) => (
                <tr key={vendor.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{vendor.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vendor.code || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vendor.country}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vendor.contact_number}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vendor.email}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs rounded-full ${vendor.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {vendor.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                    <button onClick={() => handleEdit(vendor)} className="text-primary-600 hover:text-primary-900">
                      <PencilIcon className="h-5 w-5" />
                    </button>
                    <button onClick={() => handleDelete(vendor.id)} className="text-red-600 hover:text-red-900">
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={handleModalClose} title={editingVendor ? 'Edit Vendor' : 'Add Vendor'}>
        <VendorForm vendor={editingVendor} onClose={handleModalClose} />
      </Modal>
    </div>
  );
};

export default VendorsPage;

