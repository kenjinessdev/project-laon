import api from "@/api/axios/route";
import type { Product, ProductFormValues } from "@/types";

export const productAPI = {
  // GET ALL PRODUCTS
  getAllProducts: async (): Promise<Product[]> => {
    const response = await api.get<Product[]>("/products");
    return response.data;
  },

  // GET ALL PRODUCTS (FARMER)
  getFAll: async (): Promise<Product[]> => {
    const response = await api.get<Product[]>("/farmer/products");
    return response.data;
  },

  // GET PRODUCT BY ID
  getById: async (product_id: string): Promise<Product> => {
    const response = await api.get<Product>(`/farmer/product/${product_id}`);
    return response.data;
  },

  // CREATE PRODUCT
  createProduct: async (productData: ProductFormValues): Promise<Product> => {
    const response = await api.post<Product>("/farmer/product", productData);
    return response.data;
  },

  // UPDATE PRODUCT
  updateProduct: async (product_id: string, productData: Partial<Product>) => {
    const response = await api.put<Product>(`/farmer/product/${product_id}`);
    return response.data;
  },

  // DELETE PRODUCT
  deleteProduct: async (product_id: string): Promise<void> => {
    await api.delete(`/farmer/product/${product_id}`);
  },
};
