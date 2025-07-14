import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardTitle,
  CardAction,
} from "@/components/ui/card";
import { Plus } from "lucide-react";
import type { Product } from "@/lib/types";

const Products = () => {
  return (
    <section>
      <div className="flex flex-row justify-between">
        {" "}
        <h1 className="font-bold text-2xl">Products</h1>
        <Button className="cursor-pointer">
          <Plus></Plus>
          Add Product
        </Button>
      </div>

      <div className="grid grid-cols-3 grid-rows-3 gap-12">
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
        <ProductCard
          name="testProduct"
          image="https://placehold.co/600x400"
          description="testDescription"
        />
      </div>
    </section>
  );
};

const ProductCard = ({ name, image }: Product) => {
  return (
    <Card className="p-4">
      <CardContent>
        <div>
          <img src={image} />
        </div>
      </CardContent>
      <CardTitle>{name}</CardTitle>
      <CardFooter>
        <CardAction>
          {" "}
          <Button className="cursor-pointer">View Details</Button>
        </CardAction>
      </CardFooter>
    </Card>
  );
};

export default Products;
