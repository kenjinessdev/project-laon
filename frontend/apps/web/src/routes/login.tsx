import { createFileRoute } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { z } from "zod";
import { zLoginSchema } from "@/client/zod.gen";
import { useMutation } from "@tanstack/react-query";
import { loginApiV1AuthLoginPostMutation } from "@/client/@tanstack/react-query.gen";
import { toast } from "sonner";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

export const Route = createFileRoute("/login")({
  component: RouteComponent,
});

type LoginSchemaType = z.infer<typeof zLoginSchema>;

export function LoginForm() {
  const onSubmit = (data: LoginSchemaType) => {
    useMutation({
      ...loginApiV1AuthLoginPostMutation(),
      onSuccess: (data) => {
        toast.success("Login successful", { description: "Welcome back!" });
      },
      onError: (error) => {
        toast.error("Login failed!", { description: error.message });
      },
    });
  };

  const form = useForm({
    resolver: zodResolver(zLoginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
    mode: "onChange",
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="Enter your email" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={!form.formState.isValid}>
          Login
        </Button>
      </form>
    </Form>
  );
}

function RouteComponent() {
  return <LoginForm />;
}
