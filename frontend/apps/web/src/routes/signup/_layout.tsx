import { createFileRoute, Outlet } from "@tanstack/react-router";

export const Route = createFileRoute("/signup/_layout")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="flex flex-col gap-y-8">
      <Outlet />
    </div>
  );
}
