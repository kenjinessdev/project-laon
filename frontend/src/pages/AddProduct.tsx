import React from "react";
import { z } from "zod";

const formSchema = z.object({
  productname: z.string(),
});

const AddProduct = () => {
  return <div>AddProduct</div>;
};

export default AddProduct;
