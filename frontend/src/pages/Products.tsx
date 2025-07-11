import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
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
        </Button>
      </div>

      <div className="grid grid-cols-3 grid-rows-3 gap-12">
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
        <ProductCard name="testProduct" image="https://placehold.co/600x400" />
      </div>
    </section>
  );
};

const ProductCard = ({ name, image }: Product) => {
  return (
    <Card className="p-4">
      <CardDescription>
        <div>
          <img src={image} />
        </div>
      </CardDescription>
      <CardTitle>{name}</CardTitle>
      <Button className="cursor-pointer">View Details</Button>
    </Card>
  );
};

export default Products;
