// ShoppingCart.js

import { Container, Button } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";
import CartItem from "./CartItem";
import { useContext } from "react";
import AuthContext from "../../store/auth-ctx";

const ShoppingCart = () => {
  const orderItemsHandler = () => {};
  const authCTX = useContext(AuthContext);
  const {
    cartItems,
    addItemToCart,
    removeItemFromCart,
    updateItemQuantity,
    calculateTotalPrice,
  } = useShoppingCart();

  let totalOrderSum = 0;
  if (cartItems.length) {
    totalOrderSum = cartItems.reduce((accumulator, currentItem) => {
      return accumulator + currentItem.sum;
    }, 0);
  }

  return (
    <Container>
      {cartItems.map((item, index) => (
        <div key={index}>
          <CartItem cartItem={item} />
        </div>
      ))}

      {!!cartItems.length && (
        <h5 className="card-title mt-3 mb-3 d-flex flex-row justify-content-end p-2">
          Sum:
          <span style={{ fontWeight: "bold", paddingLeft: 10 }}>
            ${totalOrderSum}
          </span>
        </h5>
      )}
      {!!cartItems.length && authCTX.isAuthenticated && (
        <Container className="card-title mt-3 mb-3 d-flex flex-row justify-content-end p-2">
          <Button variant="primary" onClick={orderItemsHandler}>
            Order items!
          </Button>
        </Container>
      )}
      {!authCTX.isAuthenticated && (
        <h3 className="d-flex flex-row text-danger justify-content-center ">
          Log in to order!
        </h3>
      )}
    </Container>
  );
};

export default ShoppingCart;
