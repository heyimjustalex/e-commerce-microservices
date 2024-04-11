import { Container, Row, Col, Button } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";

const CartItem = (props) => {
  const { name, price, quantity } = props.cartItem;
  const {
    cartItems,
    addItemToCart,
    removeItemFromCart,
    updateItemQuantity,
    calculateTotalPrice,
  } = useShoppingCart();

  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Price: ${price}</p>
              <p className="card-text">Selected quantity: {quantity}</p>
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
