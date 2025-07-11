import { useState } from "react";

import { Menu, Bell } from "lucide-react";
export const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header>
      <nav className="flex flex-row justify-between z-30">
        <Menu size={32} onClick={toggleMenu} />
        <Bell size={32} />
      </nav>
    </header>
  );
};
