import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, Bell, X } from "lucide-react";

export const MobileNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header>
      <nav className="flex flex-row justify-between z-30">
        <button onClick={toggleMenu} className="cursor-pointer">
          {isMenuOpen ? <X /> : <Menu />}
        </button>
        <Bell size={32} />
      </nav>
      {isMenuOpen && (
        <div className="fixed inset-0 z-40">
          <div
            onClick={toggleMenu}
            className="absolute inset-0 bg-orange-3/60"
          />
          <OverlayMenu />
        </div>
      )}
    </header>
  );
};

const OverlayMenu = () => {
  return (
    <nav className="w-64 sm:w-72 h-full flex flex-col bg-violet-light-9 text-violet-light-2 relative z-10 shadow-lg">
      <div className="flex flex-col p-6 pt-20 space-y-6">
        <Link
          to="/dashboard"
          className="cursor-pointer text-lg transition-colors duration-200 py-3"
        >
          <h2>Dashboard</h2>
        </Link>
        <Link
          to="/orders"
          className="cursor-pointer text-lg transition-colors duration-200 py-3"
        >
          <h2>Orders</h2>
        </Link>
        <Link
          to="/products"
          className="cursor-pointer text-lg transition-colors duration-200 py-3"
        >
          <h2>Products</h2>
        </Link>
      </div>
    </nav>
  );
};
