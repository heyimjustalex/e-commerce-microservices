import { Container } from "react-bootstrap/esm";
import { getProducts } from "../../api/api.js";
import useHttp from "../../hooks/use-http";
import LoadingRing from "../../UI/LoadingRing";
import { useEffect, useState } from "react";
import ProductElement from "./ProductElement";

const Products = () => {
  const { sendRequest, status, error, data } = useHttp(getProducts);
  const [output, setOutput] = useState({});

  useEffect(() => {
    sendRequest();
  }, [sendRequest]);

  useEffect(() => {
    if (status === "pending") {
      setOutput({ header: "Loading...", content: <LoadingRing /> });
    } else if (status === "completed" && !error) {
      setOutput({ header: "Products:", content: data });
    } else if (status === "completed" && error) {
      setOutput({ header: "Products fetching error", content: "" });
    }
  }, [status, error, setOutput, data]);

  return (
    <Container className="p-3 m-5 d-flex flex-column align-items-center justify-content-center">
      {status === "pending" && output && output.content}
      {status === "completed" && output && <h2>{output.header}</h2>}
      {status === "completed" &&
        output &&
        output.content &&
        !error &&
        output.content.products &&
        output.content.products.map((product, index) => (
          <ProductElement key={index} product={product} />
        ))}
    </Container>
  );
};
export default Products;
