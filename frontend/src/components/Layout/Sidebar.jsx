/**
 * Sidebar Navigation Component
 */

import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  CubeIcon,
  BuildingStorefrontIcon,
  UserGroupIcon,
  ShoppingCartIcon,
  BanknotesIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: HomeIcon },
    { path: '/inventory', label: 'Inventory', icon: CubeIcon },
    { path: '/vendors', label: 'Vendors', icon: BuildingStorefrontIcon },
    { path: '/clients', label: 'Clients', icon: UserGroupIcon },
    { path: '/purchases', label: 'Purchases', icon: ShoppingCartIcon },
    { path: '/sales', label: 'Sales', icon: BanknotesIcon },
    { path: '/accounts', label: 'Accounts', icon: ChartBarIcon },
  ];

  const isActive = (path) => location.pathname.startsWith(path);

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen">
      <div className="p-6">
        <h1 className="text-2xl font-bold">ERP System</h1>
      </div>
      <nav className="mt-8">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center px-6 py-3 transition-colors ${
                isActive(item.path)
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <Icon className="h-5 w-5 mr-3" />
              {item.label}
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default Sidebar;

