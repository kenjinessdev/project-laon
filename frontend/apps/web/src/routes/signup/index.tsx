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
export const Route = createFileRoute("/signup/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section className="flex flex-col items-center gap-y-4">
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
        <Card>
          <CardHeader>
            {/** ICON HERE */}
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul>
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
                <Button className="w-full">Start Shopping</Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
        <Card>
          <CardHeader>
            {/** ICON HERE */}
            <CardTitle className="text-center">I'm a Farmer</CardTitle>
            <CardDescription className="text-center">
              Sell your produce directly to customers and grow your business{" "}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul>
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
                <Button className="w-full">Start Selling</Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
      </div>

      <h1 className="font-bold text-3xl">Why Choose Laon</h1>
      <div>
        <Card>
          <CardHeader>
            {/** ICON HERE */}
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul>
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
                <Button className="w-full">Start Shopping</Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
        <Card>
          <CardHeader>
            {/** ICON HERE */}
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul>
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
                <Button className="w-full">Start Shopping</Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
        <Card>
          <CardHeader>
            {/** ICON HERE */}
            <CardTitle className="text-center">I'm a Customer</CardTitle>
            <CardDescription className="text-center">
              Buy fresh, quality produce directly from local farmers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ul>
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
                <Button className="w-full">Start Shopping</Button>
              </Link>
            </CardAction>
          </CardFooter>
        </Card>
      </div>
    </section>
  );
}
