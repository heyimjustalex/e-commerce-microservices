import { Container, Row, Col, Button } from "react-bootstrap/esm";

const ProductElement = (props) => {
  const { name, description, price, quantity } = props.product;
  const handleAddToCart = () => {
    console.log("Product added to cart:", name);
  };
  return (
    <Container>
      <Row>
        <Col>
          <div className="card m-3">
            <div className="card-body">
              <h5 className="card-title">Product: {name}</h5>
              <p className="card-text">Description: {description}</p>
              <p className="card-text">Price: ${price}</p>
              <p className="card-text">Quantity: {quantity}</p>
              <Button variant="primary" onClick={handleAddToCart}>
                Add to Cart
              </Button>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default ProductElement;
