import { Link, useLocation } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const links = [
    { path: "/", label: "Dashboard" },
    { path: "/jobs", label: "Jobs" },
    { path: "/applications", label: "Applications" },
    { path: "/profile", label: "Profile" },
  ];

  return (
    <nav className="border-b border-gray-200 bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex shrink-0 items-center">
              <span className="text-xl font-bold text-blue-600">
                JobAgent AI
              </span>
            </div>
            <div className="ml-10 flex space-x-8">
              {links.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={`inline-flex items-center border-b-2 px-1 pt-1 text-sm font-medium ${
                    location.pathname === link.path
                      ? "border-blue-500 text-gray-900"
                      : "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">{user?.full_name}</span>
            <button
              onClick={logout}
              className="rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
