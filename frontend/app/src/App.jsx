import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar/Navbar";
import LoginForm from "./components/Login/LoginForm";
import Home from "./components/Home/Home";

function App() {
  return (
    <Router>
      <div className="container-fluid">
        <Navbar />
        <div
          className="row justify-content-center align-items-center"
          style={{ minHeight: "90vh" }}
        >
          <div className="col-md-8">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<LoginForm />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}
export default App;
