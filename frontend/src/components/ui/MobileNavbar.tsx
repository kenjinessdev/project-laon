// import { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, Bell } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "./dropdown-menu";

export const MobileNavbar = () => {
  return (
    <header>
      <nav className="flex flex-row justify-between z-30">
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Menu size={32} className="cursor-pointer" />
          </DropdownMenuTrigger>
          <DropdownMenuContent sideOffset={8} align="start">
            <DropdownMenuItem asChild>
              <Link to="/dashboard">Dashboard</Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link to="/products">Products</Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link to="/orders">Orders</Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
        <Bell size={32} />
      </nav>
    </header>
  );
};
