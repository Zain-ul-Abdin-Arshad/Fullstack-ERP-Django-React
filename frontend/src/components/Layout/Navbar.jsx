/**
 * Navbar Component (Alternative to Sidebar)
 * Can be used for top navigation if needed
 */

import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/inventory', label: 'Inventory' },
    { path: '/vendors', label: 'Vendors' },
    { path: '/clients', label: 'Clients' },
    { path: '/purchases', label: 'Purchases' },
    { path: '/sales', label: 'Sales' },
  ];

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {menuItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium ${
                  location.pathname === item.path
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {item.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

