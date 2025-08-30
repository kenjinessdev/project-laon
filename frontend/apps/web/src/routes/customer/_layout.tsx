import { createFileRoute, Outlet } from "@tanstack/react-router";

export const Route = createFileRoute("/customer/_layout")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="flex flex-col space-y-8">
      <Outlet />
    </div>
  );
}
