import { Container, Button } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";
import CartItem from "./CartItem";
import { useContext, useEffect, useState } from "react";
import AuthContext from "../../store/auth-ctx";

const ShoppingCart = () => {
  const orderItemsHandler = () => {};
  const authCTX = useContext(AuthContext);
  const { cartItems } = useShoppingCart();
  const [totalOrderSum, setTotalOrderSum] = useState(0);

  useEffect(() => {
    if (cartItems.length) {
      const tempTotalOrderSum = cartItems.reduce((accumulator, currentItem) => {
        return accumulator + currentItem.sum;
      }, 0);
      setTotalOrderSum(Math.round(tempTotalOrderSum * 100) / 100);
    }
  }, [cartItems, totalOrderSum, setTotalOrderSum]);

  const updateSumHandler = () => {
    const tempTotalOrderSum = cartItems.reduce((accumulator, currentItem) => {
      return accumulator + currentItem.sum;
    }, 0);
    setTotalOrderSum(Math.round(tempTotalOrderSum * 100) / 100);
  };

  if (cartItems.length === 0) {
    return (
      <Container>
        <h3 className="d-flex flex-row text-danger justify-content-center ">
          No items in the cart!
        </h3>
      </Container>
    );
  }

  return (
    <Container>
      {cartItems.map((item, index) => (
        <div key={index}>
          <CartItem updateTotalSum={updateSumHandler} cartItem={item} />
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
