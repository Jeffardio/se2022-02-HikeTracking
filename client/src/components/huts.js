import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Container, ListGroup, Row, Col, Modal } from 'react-bootstrap';
import { useState } from 'react';
import UTILS from '../utils/utils';

function displayHutsUtil(huts) {
  let hutscard = huts.map((h, idx) =>
    <Col className="pb-4 px-0" key={idx}>
      <HutCard hut={h} />
    </Col>)
  let rows = UTILS.createRows(huts, hutscard)
  return (
    <>
      <Container>
        <Row>
          <Col xs={10}>
            <h1>All Huts</h1>
          </Col>
        </Row>
      </Container>
      <div>
        {rows}
      </div>
    </>
  )
}

function Huts(props) {
  if (props.huts.length === 0) {
    return <h1>No available huts</h1>
  }
  else {
    return displayHutsUtil(props.huts)
  }
}


function HutCard(props) {
  const [modalDescriptionShow, setModalDescriptionShow] = useState(false);
  const services = props.hut.services.join(', ')
  const hikes = props.hut.hikes.join(', ')
  return (<>
    <Card style={{ width: '22rem' }} key={0} title={props.hut.name}>
      <Card.Body>
        <Card.Title>{props.hut.name}</Card.Title>
      </Card.Body>
      <ListGroup className="list-group-flush">
        <ListGroup.Item>Address: {props.hut.address}</ListGroup.Item>
        <ListGroup.Item>Ascent: {props.hut.ascent}€</ListGroup.Item>
        <ListGroup.Item>#Beds: {props.hut.n_beds}</ListGroup.Item>
        <ListGroup.Item>Services: {services}</ListGroup.Item>
        <ListGroup.Item>Hikes: {hikes}</ListGroup.Item>
        <ListGroup.Item>Fee per night: {props.hut.fee}€</ListGroup.Item>
        <ListGroup.Item>Phone number: {props.hut.phone}</ListGroup.Item>
        <ListGroup.Item>Email: {props.hut.email}</ListGroup.Item>
        <ListGroup.Item>Web Site: {props.hut.website}</ListGroup.Item>
      </ListGroup>
      <Card.Body>
        <Card.Text>
          <Button onClick={() => setModalDescriptionShow(true)}>Description</Button>
          {' '}

        </Card.Text>
      </Card.Body>

    </Card>
    <HutModalDescription
      show={modalDescriptionShow}
      onHide={() => setModalDescriptionShow(false)}
      name={props.hut.name}
      desc={props.hut.desc}
    />

  </>
  );
}
function HutModalDescription(props) {
  return (
    <Modal
      {...props}
      size="lg"
      aria-labelledby="contained-modal-title-vcenter"
      centered
    >
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-vcenter">
          {props.name}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <h4>Description</h4>
        <p>
          {props.desc}
        </p>
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.onHide}>Close</Button>
      </Modal.Footer>
    </Modal>
  );
}



export default Huts;


