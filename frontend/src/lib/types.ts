export interface Product {
  image?: string;
  name: string;
  description: string;
}

export type OrderStatus =
  | "paid"
  | "complete"
  | "to pay"
  | "to ship"
  | "to receive"
  | "to rate";

export interface Order {
  customerName: string;
  orderPrice: number;
  orderStatus: OrderStatus;
}
