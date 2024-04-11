import React, { useContext, useEffect, useState } from "react";
import AuthContext from "../../store/auth-ctx";
import { register } from "../../lib/api";
import useHttp from "../../hooks/use-http";
import LoadingRing from "../../UI/LoadingRing";
import { useNavigate } from "react-router-dom";
import { Form, Button, Container, Row, Col } from "react-bootstrap";

const RegisterForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [output, setOutput] = useState({});
  const authCTX = useContext(AuthContext);
  const { sendRequest, data, status, error } = useHttp(register);
  const navigate = useNavigate();

  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      setOutput({ header: "Success!", content: "" });
      navigate("/login");
    } else if (status === "completed" && error) {
      setOutput({ header: "Error occurred:", content: error });
    }
  }, [status, error, setOutput, data, authCTX, navigate]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setOutput({ header: "Passwords do not match", content: "" });
      return;
    }
    const userData = { email: email, password: password };
    sendRequest(userData);
    setEmail("");
    setPassword("");
    setConfirmPassword("");
  };

  return (
    <Container>
      <h2>Register</h2>
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
        <Form.Group className="mb-3" controlId="confirmPassword">
          <Form.Label>Confirm Password:</Form.Label>
          <Form.Control
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Register
        </Button>
      </Form>
      <Container className="d-flex w-100 align-items-center justify-content-center">
        <Row className="mt-3">
          <Col>
            <h3>{output.header}</h3>
            <h3>{output.content}</h3>
          </Col>
        </Row>
      </Container>
    </Container>
  );
};

export default RegisterForm;
