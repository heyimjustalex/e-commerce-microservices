import { Container, Button } from "react-bootstrap";
import { useShoppingCart } from "../../store/cart-ctx";
import CartItem from "./CartItem";
import { useContext, useEffect, useState } from "react";
import AuthContext from "../../store/auth-ctx";
import useHttp from "../../hooks/use-http";
import { postOrderItems } from "../../api/api";
import LoadingRing from "../../UI/LoadingRing";

const ShoppingCart = () => {
  const { sendRequest, status, error, data } = useHttp(postOrderItems);
  const authCTX = useContext(AuthContext);
  const [output, setOutput] = useState({});

  const orderItemsHandler = () => {
    const cartItemOnlyQuantity = cartItems.map((item) => {
      return { name: item.name, quantity: item.quantity };
    });
    const orderItems = {
      token: authCTX.accessToken,
      products: cartItemOnlyQuantity,
    };
    sendRequest(orderItems);
  };

  const { cartItems, removeAllItems } = useShoppingCart();
  const [totalOrderSum, setTotalOrderSum] = useState(0);

  const updateSumHandler = () => {
    const tempTotalOrderSum = cartItems.reduce((accumulator, currentItem) => {
      return accumulator + currentItem.sum;
    }, 0);
    setTotalOrderSum(Math.round(tempTotalOrderSum * 100) / 100);
  };

  useEffect(() => {
    if (cartItems.length) {
      const tempTotalOrderSum = cartItems.reduce((accumulator, currentItem) => {
        return accumulator + currentItem.sum;
      }, 0);
      setTotalOrderSum(Math.round(tempTotalOrderSum * 100) / 100);
    }
  }, [cartItems, totalOrderSum, setTotalOrderSum, updateSumHandler]);

  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      setOutput({ header: "Order placed", content: data });
      removeAllItems();
    } else if (status === "completed" && error) {
      setOutput({ header: error, content: "" });
    }
  }, [status, error, setOutput, data]);

  if (cartItems.length === 0) {
    return (
      <Container className=" d-flex flex-column align-items-center justify-content-center">
        <Container className="text-success d-flex mb-4 flex-column align-items-center justify-content-center">
          {status === "pending" && output.content}
          {status === "completed" && !error && (
            <>
              <h2>{output.header}</h2>
              <h2> Order status: {data.status}</h2>
            </>
          )}
          {status === "completed" && error && <h2>{error}</h2>}
        </Container>
        <h3 className="d-flex flex-row text-danger justify-content-center ">
          No items in the cart!
        </h3>
      </Container>
    );
  }

  return (
    <Container className="d-flex  flex-column">
      {cartItems.map((item, index) => (
        <div key={item.name}>
          <CartItem
            key={item.name}
            updateTotalSum={updateSumHandler}
            cartItem={item}
          />
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
      {status === "completed" && (
        <h2 className="d-flex flex-row text-danger justify-content-center ">
          Order not placed! {output.header}
        </h2>
      )}
      <Container className="d-flex flex-row justify-content-center">
        {status === "pending" && output.content}
      </Container>
    </Container>
  );
};

export default ShoppingCart;
