import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/customer/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section className="flex flex-col gap-y-4">
      <h1>Fresh Products</h1>
      {/** TODO: SEARCH BAR */}

      <div className="grid grid-cols-2 grid-rows-6 gap-4">
        <div>1</div>
        <div>2</div>
        <div className="row-start-2">3</div>
        <div className="row-start-2">4</div>
      </div>
    </section>
  );
}
