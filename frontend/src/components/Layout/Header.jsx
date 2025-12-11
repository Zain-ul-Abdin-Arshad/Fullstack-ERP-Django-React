/**
 * Header Component
 */

import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/auth';
import { BellIcon, UserCircleIcon } from '@heroicons/react/24/outline';

const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center">
          <h2 className="text-xl font-semibold text-gray-800">ERP Management System</h2>
        </div>
        <div className="flex items-center space-x-4">
          <button className="p-2 text-gray-600 hover:text-gray-900">
            <BellIcon className="h-6 w-6" />
          </button>
          <div className="flex items-center space-x-2">
            <UserCircleIcon className="h-8 w-8 text-gray-600" />
            <span className="text-sm text-gray-700">Admin</span>
          </div>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;

