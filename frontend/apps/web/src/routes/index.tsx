import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardAction,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  component: HomeComponent,
});

function HomeComponent() {
  return (
    <section>
      <div>
        <h1>Fresh from your farm to your table</h1>
        <h2>
          Join our marketplace where farmers sell directly to customers,
          ensuring fresh produce and fair prices for everyone.
        </h2>
        <Card>
          <CardHeader>
            <CardTitle>I'm a Customer</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Buy fresh, quality produce directly from local farmers.
              <ul>
                <li>Browse fresh products from local farms.</li>
                <li>Search and filter products easily</li>
                <li>Direct communication from farmers</li>
                <li>Secure checkout and payment</li>
                <li>Rate and review products</li>
              </ul>
            </CardDescription>
            <CardAction>Start Shopping</CardAction>
          </CardContent>{" "}
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>I'm a Farmer</CardTitle>
          </CardHeader>
          <CardContent>
            <CardDescription>
              Sell your produce directly to customers and grow your business.
              <ul>
                <li>Browse fresh products from local farms.</li>
                <li>Search and filter products easily</li>
                <li>Direct communication from farmers</li>
                <li>Secure checkout and payment</li>
                <li>Rate and review products</li>
              </ul>
            </CardDescription>
            <CardAction>Start Selling</CardAction>
          </CardContent>{" "}
        </Card>
        <h2>
          Why Choose Laon?
          <Card>
            <CardTitle>Market Insights</CardTitle>
            <CardContent>
              <CardDescription>
                Real-time market data and selling recommendations.
              </CardDescription>
            </CardContent>
          </Card>
          <Card>
            <CardTitle>Secure and Trusted</CardTitle>
            <CardContent>
              <CardDescription>
                Safe payments and verified user reviews{" "}
              </CardDescription>
            </CardContent>
          </Card>
          <Card>
            <CardTitle>Direct Connection</CardTitle>
            <CardContent>
              <CardDescription>
                Connect farmers and customers without middlemen{" "}
              </CardDescription>
            </CardContent>
          </Card>
        </h2>
      </div>
    </section>
  );
}
