import React, { useState } from "react";
import { Link } from "react-router-dom";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import styles from "./Navbar.module.css";
import { Container } from "react-bootstrap/esm";

const CustomNavbar = () => {
  return (
    <Navbar
      expand="lg"
      bg="white"
      sticky="top"
      className={styles.navbarFixedTop}
      collapseOnSelect
    >
      <Navbar.Brand as={Link} to="/">
        micro-shop
      </Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Container className="d-flex justify-content-center">
          <Nav className="mx-auto">
            <Nav.Link eventKey="1" as={Link} to="/">
              Home
            </Nav.Link>
            <Nav.Link eventKey="1" as={Link} to="/orders">
              Orders
            </Nav.Link>
            <Nav.Link eventKey="2" as={Link} to="/products">
              Products
            </Nav.Link>
            <Nav.Link eventKey="3" as={Link} to="/login">
              Login
            </Nav.Link>
          </Nav>
        </Container>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default CustomNavbar;
