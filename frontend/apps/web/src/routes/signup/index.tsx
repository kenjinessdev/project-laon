import { createFileRoute, Link } from "@tanstack/react-router";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ShoppingBag, Tractor, TrendingUp, Shield, Users } from "lucide-react";
export const Route = createFileRoute("/signup/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section className="flex flex-col items-center gap-y-4 pb-8">
      <h1 className="font-bold text-4xl text-center">
        Fresh from your Farm <br />
        to your Table!
      </h1>
      <h2 className="text-center">
        Join our marketplace where farmers sell directly to customers, ensuring
        every fresh produce and fair prices for everyone.
      </h2>
      <div className="flex flex-col gap-y-8">
        {" "}
        <Card className="border-orange-400 border-2">
          <CardHeader className="flex flex-col items-center">
            <div className="bg-orange-500 rounded-full p-3 inline-flex items-center justify-center">
              <ShoppingBag size={48} color="white" />
            </div>
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside">
              <li>Browse fresh products from local farms</li>
              <li>Search and filter products easily</li>
              <li>Direct communication with farmers</li>
              <li>Secure checkout and payment</li>
              <li>Rate and review products</li>
            </ul>
          </CardContent>
          <CardFooter>
            <CardAction className="w-full">
              <Link to="/signup/customer">
                <Button className="w-full cursor-pointer bg-orange-400 hover:bg-orange-500">
                  Start Shopping
                </Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
        <Card className="border-green-400 border-2">
          <CardHeader className="flex flex-col items-center">
            <div className="bg-green-400 rounded-full p-3 inline-flex items-center justify-center">
              <Tractor size={48} color="white" />
            </div>
            <CardTitle className="text-center">I'm a Farmer</CardTitle>
            <CardDescription className="text-center">
              Sell your produce directly to customers and grow your business{" "}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="list-disc list-inside">
              <li>Manage products and inventory easily</li>
              <li>Track orders and customer communications</li>
              <li>Get market insights and trends</li>
              <li>Receive payments securely</li>
              <li>Build customer relationships</li>
            </ul>
          </CardContent>
          <CardFooter>
            <CardAction className="w-full">
              {" "}
              <Link to="/signup/farmer">
                <Button className="w-full cursor-pointer bg-green-400 hover:bg-500">
                  Start Selling
                </Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
        <h1 className="font-bold text-3xl text-center">Why Choose Laon</h1>
        <Card className="border-green-200">
          <CardHeader className="flex flex-col items-center">
            <TrendingUp size={48} color="green" />
            <CardTitle className="text-center">Market Insights</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
        </Card>
        <Card className="border-green-200">
          <CardHeader className="flex flex-col items-center">
            <Shield size={48} color="blue" />
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
        </Card>
        <Card className="border-green-200">
          <CardHeader className="flex flex-col items-center">
            <Users size={48} color="orange" />
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </section>
  );
}
