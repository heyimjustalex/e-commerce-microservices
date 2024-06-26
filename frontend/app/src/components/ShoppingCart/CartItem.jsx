import { Container, Row, Col, Button, Card, Form } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";
import { useState } from "react";

const CartItem = (props) => {
  const { name, price, quantity, sum } = props.cartItem;
  const [newQuantity, setNewQuantity] = useState(quantity);
  const { removeItemFromCart, updateItemQuantity } = useShoppingCart();

  const handleItemRemoval = () => {
    setNewQuantity(0);
    removeItemFromCart(name);
    props.updateTotalSum();
  };

  const handleQuantityChange = (e) => {
    const updatedQuantity = parseInt(e.target.value);
    setNewQuantity(updatedQuantity);
    updateItemQuantity(name, updatedQuantity);
    props.updateTotalSum();
  };

  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Price: ${price}</p>
              <p className="card-text">Sum: ${sum}</p>
              <Card.Text>
                Quantity:
                <Form.Control
                  type="number"
                  value={newQuantity}
                  min={1}
                  onChange={handleQuantityChange}
                />
              </Card.Text>
              <Button
                variant="danger"
                onClick={(e) => {
                  handleItemRemoval();
                }}
              >
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
