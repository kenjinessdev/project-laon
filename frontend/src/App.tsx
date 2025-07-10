import "./index.css";
import { router } from "./routes/routes";
import { RouterProvider } from "react-router-dom";

export const App = () => {
  return <RouterProvider router={router} />;
};
