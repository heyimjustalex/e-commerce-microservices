import { Container } from "react-bootstrap/esm";
import { getOrders } from "../../lib/api";
import useHttp from "../../hooks/use-http";
import LoadingRing from "../../UI/LoadingRing";
import { useEffect, useState } from "react";
import OrderElement from "./OrderElement";

const Orders = () => {
  const { sendRequest, status, error, data } = useHttp(getOrders);
  const [output, setOutput] = useState({});

  useEffect(() => {
    sendRequest();
  }, [sendRequest]);

  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      setOutput({ header: "Orders:", content: data });
      console.log(data.orders);
    } else if (status === "completed" && error) {
      setOutput({ header: "Orders fetching error", content: "" });
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
        output.content.orders.map((order, index) => (
          <OrderElement key={index} order={order} />
        ))}
    </Container>
  );
};

export default Orders;
