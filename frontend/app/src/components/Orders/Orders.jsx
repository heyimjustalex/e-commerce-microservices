import { Container } from "react-bootstrap/esm";
import { getOrders } from "../../api/api.js";
import useHttp from "../../hooks/use-http.js";
import LoadingRing from "../../UI/LoadingRing";
import { useContext, useEffect, useState } from "react";
import OrderElement from "./OrderElement";
import AuthContext from "../../store/auth-ctx";

const Orders = () => {
  const authCTX = useContext(AuthContext);
  const { sendRequest, status, error, data } = useHttp(getOrders);
  const [output, setOutput] = useState({});

  useEffect(() => {
    sendRequest(authCTX.accessToken);
  }, [sendRequest]);

  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      setOutput({ header: "Orders:", content: data });
    } else if (status === "completed" && error) {
      setOutput({ header: error, content: "" });
    }
  }, [status, error, setOutput, data]);

  return (
    <Container className="p-3 m-5 d-flex flex-column align-items-center justify-content-center">
      {status === "pending" && output.content}
      {status === "completed" && <h2>{output.header}</h2>}
      {status === "completed" &&
        !error &&
        output.content &&
        output.content.orders &&
        output.content.orders
          .reverse()
          .map((order, index) => (
            <OrderElement index={index} key={index} order={order} />
          ))}
    </Container>
  );
};

export default Orders;
