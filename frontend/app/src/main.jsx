import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";
import { AuthContextProvider } from "./store/auth-ctx";
import { ShoppingCartProvider } from "./store/cart-ctx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <ShoppingCartProvider>
    <AuthContextProvider>
      <App />
    </AuthContextProvider>
  </ShoppingCartProvider>
);
