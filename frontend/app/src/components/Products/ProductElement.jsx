import { Container, Row, Col, Button, Form } from "react-bootstrap/esm";
import ShoppingCart from "../ShoppingCart/ShoppingCart";
import { useShoppingCart } from "../../store/cart-ctx";
import { useState } from "react";

const ProductElement = (props) => {
  const [selectedQuantity, setSelectedQuantity] = useState(1);
  const [message, setMessage] = useState("");

  const { name, description, price, quantity } = props.product;
  const { addItemToCart } = useShoppingCart();

  const handleAddToCart = () => {
    addItemToCart({ name: name, quantity: selectedQuantity, price: price });
    setSelectedQuantity(1);
    setMessage("Product added to cart!");
    setTimeout(() => {
      setMessage("");
    }, 1000);
  };

  const handleQuantityChange = (e) => {
    const newQuantity = parseInt(e.target.value);
    setSelectedQuantity(newQuantity);
  };
  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Description: {description}</p>
              <p className="card-text">Price: ${price}</p>
              <p className="card-text">Avaliable: {quantity}</p>
              <Form.Group controlId="quantity">
                <Form.Label>Quantity:</Form.Label>
                <Form.Control
                  type="number"
                  min={1}
                  max={quantity}
                  value={selectedQuantity}
                  onChange={handleQuantityChange}
                />
              </Form.Group>
              <Button
                className="m-3"
                disabled={!quantity}
                variant="primary"
                onClick={handleAddToCart}
              >
                Add to Cart
              </Button>
              <h5 className="text-success"> {message}</h5>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default ProductElement;
