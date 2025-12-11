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
  TruckIcon,
} from '@heroicons/react/24/outline';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: HomeIcon },
    { path: '/inventory', label: 'Inventory', icon: CubeIcon },
    { path: '/vendors', label: 'Vendors', icon: BuildingStorefrontIcon },
    { path: '/clients', label: 'Clients', icon: UserGroupIcon },
    { path: '/purchases', label: 'Purchases', icon: ShoppingCartIcon },
    { path: '/sales', label: 'Sales', icon: TruckIcon },
  ];

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="w-64 bg-gray-800 text-white flex flex-col">
      {/* Logo */}
      <div className="h-16 flex items-center justify-center border-b border-gray-700">
        <h1 className="text-xl font-bold">ERP System</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-4 space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                active
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-700 hover:text-white'
              }`}
            >
              <Icon className="w-5 h-5 mr-3" />
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default Sidebar;

