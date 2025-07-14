import React from "react";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Avatar, AvatarImage } from "@/components/ui/avatar";
import { Eye, MessagesSquare } from "lucide-react";
import type { Order } from "@/lib/types";
import { Button } from "@/components/ui/button";

const Orders = () => {
  return (
    <section>
      <h1 className="text-2xl font-bold">Orders</h1>
      <div className="grid grid-rows-5 gap-4">
        <OrderCard
          customerImage="https://github.com/shadcn.png"
          orderCode="ORD-001"
          customerName="Haru Urara"
          orderPrice={10000}
          orderStatus="PAID"
          orderDate="July 3, 2025"
        />
      </div>
    </section>
  );
};

const OrderCard = ({
  customerName,
  orderCode,
  orderStatus,
  orderPrice,
  customerImage,
  orderDate,
}: Order) => {
  return (
    <Card>
      {/** HEADER SIDE */}
      <CardHeader className="flex flex-row justify-between">
        <div className="flex flex-row gap-2 items-center">
          {" "}
          <Avatar>
            <AvatarImage src={customerImage} />{" "}
          </Avatar>{" "}
          <div className="flex flex-col">
            <h1 className="text-lg">{orderCode}</h1>
            <h1 className="text-lg">{customerName}</h1>
            <h1 className="text-lg">{orderDate}</h1>
          </div>
        </div>

        <div className="flex flex-col justify-between gap-4">
          <h2>{orderPrice}</h2>
          <Badge>{orderStatus}</Badge>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-6">
        <Button variant="outline">
          <Eye />
          View Details
        </Button>
        <Button variant="outline">
          <MessagesSquare />
          Message Customer
        </Button>
      </CardContent>
      <CardFooter>
        <Button className="flex w-full">Update Status</Button>
      </CardFooter>
    </Card>
  );
};

export default Orders;
