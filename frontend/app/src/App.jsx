import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CustomNavbar from "./components/Navbar/Navbar";
import LoginForm from "./components/Login/LoginForm";
import Home from "./components/Home/Home";
import "bootstrap/dist/css/bootstrap.min.css";
import Products from "./components/Products/Products";
import Orders from "./components/Orders/Orders";
import RegisterForm from "./components/Register/RegisterForm";
import ShoppingCart from "./components/ShoppingCart/ShoppingCart";
import CreateProduct from "./components/Products/CreateProduct";
function App() {
  return (
    <Router>
      <div className="container-fluid">
        <CustomNavbar />
        <div
          className="row justify-content-center align-items-center"
          style={{ minHeight: "90vh" }}
        >
          <div className="col-md-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<LoginForm />} />
              <Route path="/products" element={<Products />} />
              <Route path="/orders" element={<Orders />} />
              <Route path="/register" element={<RegisterForm />} />
              <Route path="/shopping-cart" element={<ShoppingCart />} />
              <Route path="/add-product" element={<CreateProduct />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}
export default App;
