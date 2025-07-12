import { MobileNavbar } from "@/components/ui/MobileNavbar";
import { Outlet } from "react-router";
export const Layout = () => {
  return (
    <div className="flex flex-col max-w-2xl w-full m-auto py-4">
      <MobileNavbar />
      <main className="flex-col justify-between py-8">
        <Outlet />
      </main>
    </div>
  );
};
