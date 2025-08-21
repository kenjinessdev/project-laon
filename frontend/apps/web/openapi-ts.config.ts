import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "http://localhost:8000/openapi.json", // FastAPI spec
  output: "src/client", // where SDK is generated
  plugins: [
    "@hey-api/typescript", // generate TypeScript types
    "@hey-api/client-axios", // generate Axios-based client
    "@tanstack/react-query", // generate TanStack Query hooks
    "zod",
  ],
});
