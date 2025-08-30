import { createFileRoute } from "@tanstack/react-router";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  TrendingUp,
  ShoppingCart,
  PhilippinePeso,
  Box,
  ChartColumn,
  CircleAlert,
} from "lucide-react";
export const Route = createFileRoute("/dashboard")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section className="flex flex-col justify-between">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="grid grid-cols-2 grid-rows-5 gap-4">
        <div>
          <Card className="px-6">
            <CardTitle className="font-bold text-lg">New Orders</CardTitle>
            <CardDescription className="flex flex-row justify-between items-center">
              2
              <ShoppingCart color="green" />
            </CardDescription>
          </Card>
        </div>
        <div className="col-start-1 row-start-2">
          <Card className="px-6">
            <CardTitle className="font-bold text-lg">Revenue</CardTitle>
            <CardDescription className="flex flex-row justify-between items-center">
              <PhilippinePeso />
              123456.00
            </CardDescription>
            <PhilippinePeso />
          </Card>
        </div>
        <div className="col-start-2 row-start-1">
          <Card className="px-6">
            <CardTitle className="font-bold text-lg">Products</CardTitle>
            <CardDescription className="flex flex-row justify-between items-center">
              5
              <Box />
            </CardDescription>
          </Card>
        </div>
        <div className="row-start-2">
          <Card className="px-6 ">
            <CardTitle className="font-bold text-lg">Low Stock</CardTitle>
            <CardDescription className="flex flex-row justify-between items-center">
              1
              <CircleAlert />
            </CardDescription>
          </Card>
        </div>
        <div className="col-span-2 row-start-3">
          <Card className="px-6">
            <CardTitle className="font-bold text-lg flex flex-row items-center gap-2">
              <ChartColumn />
              Sales Chart
            </CardTitle>
            <CardDescription>
              <div className="flex flex-row justify-between">
                <p>This week</p>
                <div>Filler bar</div>
              </div>
              <div className="flex flex-row justify-between">
                <p>Last week</p>
                <div>Filler bar</div>
              </div>
            </CardDescription>
          </Card>
        </div>
        <div className="col-span-2 row-start-4">
          <Card className="px-6">
            <CardTitle className="font-bold text-lg flex flex-row items-center gap-2">
              <TrendingUp />
              Price Updates
            </CardTitle>
            <CardDescription>
              <div className="flex flex-row justify-between">
                <p>Fresh Tomatoes</p>
                <p>P10.00</p>
              </div>
              <div className="flex flex-row justify-between">
                <p>Fresh Tomatoes</p>
                <p>P10.00</p>
              </div>
              <div className="flex flex-row justify-between">
                <p>Fresh Tomatoes</p>
                <p>P10.00</p>
              </div>
            </CardDescription>
          </Card>
        </div>
      </div>
    </section>
  );
}
