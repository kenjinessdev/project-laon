import { createFileRoute, Outlet } from "@tanstack/react-router";

export const Route = createFileRoute("/signup/_layout")({
  component: RouteComponent,
});

function RouteComponent() {
  return <Outlet />;
}
