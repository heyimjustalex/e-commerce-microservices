import { Container, Row, Col, Button } from "react-bootstrap/esm";
import ProductElementStub from "./ProductElementStub";

const OrderElement = (props) => {
  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Order:</h5>

              {props.order.products &&
                props.order.products.map((product, index) => (
                  <ProductElementStub key={index} product={product} />
                ))}
              <h5 className="card-title">
                Order status:{" "}
                <span
                  style={{
                    fontWeight: "bold",
                    color:
                      props.order.status === "ACCEPTED"
                        ? "green"
                        : props.order.status === "PENDING"
                        ? "orange"
                        : props.order.status === "REJECTED"
                        ? "red"
                        : "inherit",
                  }}
                >
                  {props.order.status}
                </span>
              </h5>
              <h5 className="card-title">
                Sum:
                <span style={{ fontWeight: "bold" }}> ${props.order.cost}</span>
              </h5>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default OrderElement;
