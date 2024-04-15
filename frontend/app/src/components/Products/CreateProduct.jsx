import React, { useState, useEffect, useContext } from "react";
import { Form, Button, Container } from "react-bootstrap";
import { getCategories, postProductCreate } from "../../lib/api";
import useHttp from "../../hooks/use-http";
import AuthContext from "../../store/auth-ctx";
import LoadingRing from "../../UI/LoadingRing";

const CreateProduct = (props) => {
  const authCTX = useContext(AuthContext);
  const [output, setOutput] = useState({});

  const {
    sendRequest: sendCategoryRequest,
    data: categoryData,
    status: categoryStatus,
    error: categoryError,
  } = useHttp(getCategories);

  const {
    sendRequest: sendProductCreateRequest,
    status: productCreateStatus,
    error: productCreateError,
  } = useHttp(postProductCreate);

  const [formValues, setFormValues] = useState({
    name: "",
    description: "",
    price: 0,
    quantity: 0,
    category: "",
  });
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    sendCategoryRequest();
  }, [sendCategoryRequest]);

  useEffect(() => {
    if (categoryStatus === "completed" && !categoryError) {
      setCategories(categoryData.categories);
    }
  }, [categoryStatus, categoryError, categoryData]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormValues({
      ...formValues,
      [name]: value,
    });
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    const transformedData = {
      product: {
        name: formValues.name,
        description: formValues.description,
        price: parseFloat(formValues.price),
        quantity: parseInt(formValues.quantity),
        categories: [formValues.category],
      },
      token: authCTX.accessToken,
    };
    sendProductCreateRequest(transformedData);
  };

  useEffect(() => {
    if (productCreateStatus === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (productCreateStatus === "completed" && !productCreateError) {
      setFormValues({
        name: "",
        description: "",
        price: 0,
        quantity: 0,
        category: "",
      });
      setOutput({ header: "Product created!", content: null });
    } else if (productCreateStatus === "completed" && productCreateError) {
      setOutput({ header: productCreateError, content: null });
    }
  }, [productCreateStatus, productCreateError]);

  return (
    <div>
      <h1>Add Product</h1>
      <Container className="d-flex justify-content-center">
        {productCreateStatus === "pending" && output.content}
        {productCreateStatus === "completed" && (
          <h2 className={productCreateError ? "text-error" : "text-success"}>
            {output.header}
          </h2>
        )}
      </Container>

      <Form onSubmit={handleFormSubmit}>
        <Form.Group controlId="productName">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            name="name"
            value={formValues.name}
            onChange={handleInputChange}
            placeholder="Enter product name"
          />
        </Form.Group>

        <Form.Group controlId="productDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control
            as="textarea"
            name="description"
            value={formValues.description}
            onChange={handleInputChange}
            rows={3}
            placeholder="Enter product description"
          />
        </Form.Group>

        <Form.Group controlId="productPrice">
          <Form.Label>Price</Form.Label>
          <Form.Control
            type="number"
            name="price"
            value={formValues.price}
            onChange={handleInputChange}
            placeholder="Enter product price"
          />
        </Form.Group>

        <Form.Group controlId="productQuantity">
          <Form.Label>Quantity</Form.Label>
          <Form.Control
            type="number"
            name="quantity"
            value={formValues.quantity}
            onChange={handleInputChange}
            placeholder="Enter product quantity"
          />
        </Form.Group>

        <Form.Group controlId="productCategory">
          <Form.Label>Category</Form.Label>
          <Form.Select
            name="category"
            value={formValues.category}
            onChange={handleInputChange}
          >
            <option value="">Select a category</option>
            {categories.map((category) => (
              <option key={category.name} value={category.name}>
                {category.name}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Button
          className="mt-3"
          variant="primary"
          type="submit"
          onClick={handleFormSubmit}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
};

export default CreateProduct;
