// Product
export interface Product {
  id: string;
  name: string;
  description: string;
  category_id?: number;
  unit: string;
  price_per_unit: string;
  stock_quantity: number;
  status: "draft" | "active" | "archived" | "sold";
  visibility: "public" | "private" | "admin_only";
  user?: any;
  images?: any[];
  reviews?: any[];
}

export interface ProductDTO extends Product {
  id: string;
  name: string;
  description: string;
  category_id?: number;
  unit: string;
  price_per_unit: string;
  stock_quantity: number;
  status: "draft" | "active" | "archived" | "sold";
  visibility: "public" | "private" | "admin_only";
  user?: any;
  images?: any[];
  reviews?: any[];
}

export interface ProductFormValues {
  name: string;
  description: string;
  category_id?: number;
  unit: string;
  price_per_unit: string;
  stock_quantity: number;
  status: "draft" | "active" | "archived" | "sold";
  visibility: "public" | "private" | "admin_only";
  user?: any;
  images?: any[];
  reviews?: any[];
}

// User
export interface User {
  id: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  suffix?: string;
  profile_image_url?: string;
  email: string;
  password: string;
  phone_number: string;
  gender?: string;
  birthday: string;
  role: "farmer" | "customer";
}

export interface UserDTO extends User {
  id: string;
  first_name: string;
  middle_name?: string;
  last_name: string;
  suffix?: string;
  profile_image_url?: string;
  email: string;
  password: string;
  phone_number: string;
  gender?: string;
  birthday: string;
  role: "farmer" | "customer";
}

export interface UserFormValues {
  first_name: string;
  middle_name?: string;
  last_name: string;
  suffix?: string;
  profile_image_url?: string;
  email: string;
  password: string;
  phone_number: string;
  gender?: string;
  birthday: string;
  role: "farmer" | "customer";
}

// Order
export interface Order {}

export interface OrderDTO extends Order {}

export interface OrderFormValues {}
