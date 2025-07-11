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
import type { Order } from "@/lib/types";

const Orders = () => {
  return (
    <section>
      <h1 className="text-2xl font-bold">Orders</h1>

      <div className="grid grid-rows-5 gap-4">
        <OrderCard
          customerName="testCustomer"
          orderStatus="paid"
          orderPrice={100000}
        />
        <OrderCard
          customerName="testCustomer"
          orderStatus="paid"
          orderPrice={100000}
        />
        <OrderCard
          customerName="testCustomer"
          orderStatus="paid"
          orderPrice={100000}
        />
        <OrderCard
          customerName="testCustomer"
          orderStatus="paid"
          orderPrice={100000}
        />
        <OrderCard
          customerName="testCustomer"
          orderStatus="paid"
          orderPrice={100000}
        />
      </div>
    </section>
  );
};

const OrderCard = ({ customerName, orderStatus, orderPrice }: Order) => {
  return (
    <Card>
      <CardTitle>{customerName}</CardTitle>
      <CardDescription>
        {orderStatus}
        {orderPrice}
      </CardDescription>
    </Card>
  );
};

export default Orders;
