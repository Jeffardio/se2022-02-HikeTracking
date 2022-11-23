import { Container, Form, Row, Button, Card, InputGroup, Col, Alert } from "react-bootstrap"
import SidebarMenu from 'react-bootstrap-sidebar-menu';
import { json, useNavigate } from 'react-router-dom';
import { useEffect, useState } from "react";
import API from '../API';
import Map from './map'
import Hike from "./hikes";
import Multiselect from 'multiselect-react-dropdown';





function ParkingLotForm(props) {
  const [name, setName] = useState('Parcheggio bello')
  const [position, setPosition] = useState([45.178562524475275, 7.081797367594325])
  const [address, setAddress] = useState('Frazione Il Parcheggio 10059 Mompantero, Susa TO')
  const [desc, setDesc] = useState('First Parking lot to be uploaded')
  const [fee, setFee] = useState(10)
  const [n_cars,setNCars] = useState(10)
  let [errorMessage, setErrorMessage] = useState('')
  let navigate = useNavigate();
  let [huts, setHuts] = useState([])
  let [parkingLots, setParkingLots] = useState([])

  let token = localStorage.getItem("token");

  const handleSubmit = async (event) => {
    event.preventDefault();
    let hutDescription = {
      'name': name,
      'fee': fee,
      'desc': desc,
      'address': address,
      'latitude': position[0],
      'longitude': position[1],
      'n_cars': n_cars
    }
    let req = await API.createHut(hutDescription, token)
    console.log(req)
    if (req.error) {
      setErrorMessage(req.msg)
    } else {
      navigate('/')
    }

  }


  const checkNum = (num) => {
    if (!isNaN(num)) {
      return true;
    }
    return false
  }
  const setPoint = (point) => {
    if (!isNaN(point[0]) && !isNaN(point[1])) {
    
        setPosition(point)

    }
  }

  

  

  


  useEffect(() => {
    const getHuts = async function () {
      let req = await API.getAllHuts(token)
      if (req.error) {
        setErrorMessage(req.msg)
      } else {
        let all_huts = []
        req.msg.forEach((el) => all_huts.push({ "hutId": el.id, "hutName": el.name, "lat": el.lat, "lon": el.lon }))
        setHuts(all_huts)
      }
    }

    getHuts()
  }, [])

  /*useEffect(() => {
    const getParkingLots = async function () {
      let req = await API.getAllParkingLots(token)
      if (req.error) {
        setErrorMessage(req.msg)
      } else {
        let all_plot = []
        req.msg.forEach((el) => all_plot.push({ "parkingLotId": el.id, "parkingLotName": el.name, "lat": el.lat, "lon": el.lon }))
        setParkingLots(all_plot)
      }
    }

    getParkingLots()
  }, [])*/


  return (
    <Card body>
      <Form>
        <Form.Group className="mb-2" controlId="name">
          <Form.Label>Name</Form.Label>
          <Form.Control type="text" placeholder="Enter name" value={name} onChange={(e) => setName(e.target.value)} />
        </Form.Group>
        <Form.Group className="mb-2" controlId="fee">
          <Form.Label>Fee per hour (in €)</Form.Label>
          <Form.Control type="text" placeholder="Fee" value={fee} onChange={(e) => { if (checkNum(e.target.value)) { setFee(e.target.value) } }} />
        </Form.Group>
        <Form.Group className="mb-2" controlId="n_cars">
          <Form.Label>Number of parking spaces</Form.Label>
          <Form.Control type="text" placeholder="n_car" value={n_cars} onChange={(e) => { if (checkNum(e.target.value)) { setNCars(e.target.value) } }} />
        </Form.Group>
        
        
        <PointInput point={position} setPoint = {setPosition} address={address} setAddress={setAddress} />
       
        {' '}
        <Button variant="primary" type="submit" onClick={handleSubmit}>
          Submit
        </Button>
      </Form>
      {errorMessage ? <Alert variant='danger' onClose={() => setErrorMessage('')} dismissible >{errorMessage}</Alert> : false}
    </Card>

  )

}



function PointInput(props) {
  
  return (
    <Row className="mb-3">
            <Form.Label htmlFor="basic-url">Position</Form.Label>

      <Col>
      <InputGroup size="sm" >
        <InputGroup.Text id="inputGroup-sizing-default" >
          Lat
        </InputGroup.Text>
        <Form.Control
          aria-label="Default"
          aria-describedby="inputGroup-sizing-default"
          value={props.point[0]} onChange={(e) => props.setPoint([e.target.value, props.point[1]], props.which)}
        />
      </InputGroup>
    </Col>
      <Col>
        <InputGroup size="sm" className="">
          <InputGroup.Text id="inputGroup-sizing-default">
            Lng
          </InputGroup.Text>
          <Form.Control
            aria-label="Default"
            aria-describedby="inputGroup-sizing-default"
            value={props.point[1]} onChange={(e) => props.setPoint([props.point[0], e.target.value], props.which)}
          />
        </InputGroup>
      </Col>
      <Col>
        <InputGroup size="sm" className="">
          <InputGroup.Text id="inputGroup-sizing-default">
            Addr
          </InputGroup.Text>
          <Form.Control
            aria-label="Default"
            aria-describedby="inputGroup-sizing-default"
            value={props.address}
            onChange={(e) => props.setAddress(e.target.value)}
          />
        </InputGroup>
      </Col>
    </Row>

  )
}

export default ParkingLotForm