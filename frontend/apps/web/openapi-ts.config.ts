import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8000/openapi.json", // FastAPI spec
  output: "src/api/client", // where SDK is generated
  plugins: [
    "@hey-api/client-axios", // generate Axios-based client
    "@tanstack/react-query", // generate TanStack Query hooks
    {
      asClass: true,
      name: "@hey-api/sdk",
      validator: "zod",
    },
  ],
});
