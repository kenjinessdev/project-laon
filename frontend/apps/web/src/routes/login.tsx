import { createFileRoute } from "@tanstack/react-router";
import { useForm } from "@tanstack/react-form";
import { zodValidator } from "@tanstack/zod-validator";
import { zLoginSchema, zLoginApiV1AuthLoginPostData } from "@/client/zod.gen"; // Import the Zod schema
import { loginApiV1AuthLoginPost } from "@/client/sdk.gen"; // Import the API call
import { z } from "zod";

export const Route = createFileRoute("/login")({
  component: RouteComponent,
});

// Infer the TypeScript type from the Zod schema
type LoginSchemaType = z.infer<typeof zLoginSchema>;

export function LoginForm() {
  const form = useForm<LoginSchemaType>({
    defaultValues: {
      email: "",
      password: "",
    },
    validator: zodValidator({ schema: zLoginSchema }),
    onSubmit: async (values) => {
      try {
        // Use the generated API call
        const response = await loginApiV1AuthLoginPost({
          body: values,
        });

        // Handle successful login (e.g., redirect, store token)
        console.log("Login successful!", response);
      } catch (error) {
        // Handle login error (e.g., display error message)
        console.error("Login failed:", error);
        form.setError("root", "Invalid credentials");
      }
    },
  });

  return (
    <form onSubmit={form.handleSubmit}>
      <div>
        <label htmlFor="email">Email:</label>
        <input type="email" id="email" {...form.register("email")} />
        {form.fieldErrors.email && <div>{form.fieldErrors.email}</div>}
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input type="password" id="password" {...form.register("password")} />
        {form.fieldErrors.password && <div>{form.fieldErrors.password}</div>}
      </div>
      <button type="submit" disabled={!form.isValid}>
        Login
      </button>
      {form.options.errorMessage && <div>{form.options.errorMessage}</div>}
    </form>
  );
}

function RouteComponent() {
  return (
    <section>
      <h1>Login</h1>
      <LoginForm />
    </section>
  );
}
