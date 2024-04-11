import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import CustomNavbar from "./components/Navbar/Navbar";
import LoginForm from "./components/Login/LoginForm";
import Home from "./components/Home/Home";
import "bootstrap/dist/css/bootstrap.min.css";
import Products from "./components/Products/Products";

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
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}
export default App;
