import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../../store/auth-ctx";
import { login } from "../../lib/api";
import useHttp from "../../hooks/use-http";
import LoadingRing from "../../UI/LoadingRing";
import { useNavigate } from "react-router-dom/dist";
import { Form, Button, Container, Row, Col } from "react-bootstrap";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [output, setOutput] = useState({});
  const authCTX = useContext(AuthContext);
  const { sendRequest, data, status, error } = useHttp(login);
  const navigate = useNavigate();
  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      authCTX.login(data.access_token);
      setOutput({ header: "Success!", content: "" });
      navigate("/orders");
    } else if (status === "completed" && error) {
      setOutput({ header: "Error occured:", content: error });
    }
  }, [status, error, setOutput, data, authCTX]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const userData = { email: email, password: password };
    console.log("Submitted:", userData);
    sendRequest(userData);
    setEmail("");
    setPassword("");
  };

  return (
    <Container>
      <h2>Login</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Email:</Form.Label>
          <Form.Control
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="password">
          <Form.Label>Password:</Form.Label>
          <Form.Control
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
      <Container>
        <Row>
          <Col>
            <h3>{output.header}</h3>
            <h3>{output.content}</h3>
          </Col>
        </Row>
      </Container>
    </Container>
  );
};

export default LoginForm;
