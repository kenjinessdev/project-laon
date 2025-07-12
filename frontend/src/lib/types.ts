export interface Product {
  image?: string;
  name: string;
  description: string;
}

export type OrderStatus =
  | "PAID"
  | "COMPLETE"
  | "PENDING"
  | "TO SHIP"
  | "TO RECEIVE"
  | "TO RATE";

export interface Order {
  customerImage: string;
  orderCode: string;
  customerName: string;
  orderPrice: number;
  orderStatus: OrderStatus;
  orderDate: string;
}
