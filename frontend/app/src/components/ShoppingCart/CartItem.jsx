import { Container, Row, Col, Button, Card, Form } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";
import { useState } from "react";

const CartItem = (props) => {
  const { name, price, quantity } = props.cartItem;
  const [newQuantity, setNewQuantity] = useState(quantity);

  const { cartItems, addItemToCart, removeItemFromCart, updateItemQuantity } =
    useShoppingCart();

  const handleQuantityChange = (e) => {
    const updatedQuantity = parseInt(e.target.value);
    setNewQuantity(updatedQuantity);
    updateItemQuantity(name, updatedQuantity);
  };

  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Price: ${price}</p>
              <Card.Text>
                Quantity:
                <Form.Control
                  type="number"
                  value={newQuantity}
                  onChange={handleQuantityChange}
                />
              </Card.Text>
              <Button variant="danger" onClick={() => removeItemFromCart(name)}>
                Remove
              </Button>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default CartItem;
