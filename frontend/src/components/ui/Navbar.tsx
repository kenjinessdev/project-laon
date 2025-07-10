import { Menu, Bell } from "lucide-react";
export const Navbar = () => {
  return (
    <header>
      <nav className="flex flex-row justify-between">
        <Menu size={32} />
        <Bell size={32} />
      </nav>
    </header>
  );
};
