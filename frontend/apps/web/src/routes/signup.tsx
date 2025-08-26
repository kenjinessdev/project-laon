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
export const Route = createFileRoute("/signup")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <section className="flex-col">
      <h1>Fresh from your Farm to your Table!</h1>
      <h2>
        Join our marketplace where farmers sell directly to customers, ensuring
        every fresh produce and fair prices for everyone.
      </h2>
      <Card>
        <CardHeader>
          {/** ICON HERE */}
          <CardTitle>I'm a Customer</CardTitle>
          <CardDescription>
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
          <CardAction>Start Shopping</CardAction>
        </CardFooter>
      </Card>
      <Card>
        <CardHeader>
          {/** ICON HERE */}
          <CardTitle>I'm a Farmer</CardTitle>
          <CardDescription>
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
          <CardAction>Start Selling</CardAction>
        </CardFooter>
      </Card>
      <h1>Why Choose Laon</h1>
      <Card>
        <CardHeader>
          {/** ICON HERE */}
          <CardTitle>Market Insights</CardTitle>
          <CardDescription>
            Real-time market data and selling recommendations.{" "}
          </CardDescription>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          {/** ICON HERE */}
          <CardTitle>Secure and Trusted</CardTitle>
          <CardDescription>
            Safe payments and verified user reviews.{" "}
          </CardDescription>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          {/** ICON HERE */}
          <CardTitle>Direct Connection</CardTitle>
          <CardDescription>
            Connect farmers and customers without middlemen.{" "}
          </CardDescription>
        </CardHeader>
      </Card>
    </section>
  );
}
