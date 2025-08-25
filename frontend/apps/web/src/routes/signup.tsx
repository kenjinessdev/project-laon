import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/signup")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section>
      <h1>Signup</h1>
      <div></div>
    </section>
  );
}
