import { Container, Row, Col, Button } from "react-bootstrap/esm";

const ProductElementStub = (props) => {
  const { name, price, quantity } = props.product;

  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Price: ${price}</p>
              <p className="card-text">Quantity: {quantity}</p>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default ProductElementStub;
