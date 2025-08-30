import { Link } from "@tanstack/react-router";
import { ModeToggle } from "./mode-toggle";
import { Menu, Bell, BellDot } from "lucide-react";

export default function Header() {
  const links = [
    { to: "/", label: "Home" },
    {
      to: "/signup",
      label: "Signup",
    },
    {
      to: "/dashboard",
      label: "Dashboard",
    },
    {
      to: "/login",
      label: "Login",
    },
  ] as const;

  return (
    // <div>
    // 	<div className="flex flex-row items-center justify-between px-2 py-1">
    // 		<nav className="flex gap-4 text-lg">
    // 			{links.map(({ to, label }) => {
    // 				return (
    // 					<Link key={to} to={to}>
    // 						{label}
    // 					</Link>
    // 				);
    // 			})}
    // 		</nav>
    // 		<div className="flex items-center gap-2">
    // 			<ModeToggle />
    // 		</div>
    // 	</div>
    // 	<hr />
    // </div>
    <header>
      {" "}
      <nav className="flex flex-row justify-between px-8 py-6">
        <Menu
          onClick={() => {
            // TODO: ADD ROUTES HERE, ROUTE NAVIGATION IS DONE MANUALLY
          }}
        />{" "}
        <Bell />{" "}
      </nav>
    </header>
  );
}
