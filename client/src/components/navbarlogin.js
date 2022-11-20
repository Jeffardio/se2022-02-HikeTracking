import {Navbar, Container, Nav, Button} from 'react-bootstrap';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';

function MyNavbar2(props){
      return ( props.loggedIn ? <NavLogout logout={props.logout} userPower={props.userPower}/> : <NavLogin login={props.login} signIn={props.signIn}/>);

  function NavLogin(props){
    const navigate = useNavigate();

    return(
    <Navbar  bg="dark" variant="dark">
        <Container fluid>
             <Nav>
             
              <Navbar.Brand onClick={() => navigate("/")}>Welcome</Navbar.Brand> 
              <Button onClick={()=> props.login()} as="input" type="button" value="Login" variant='dark' size='sm'/>{' '}   
              <Button onClick={()=> props.signIn()} as="input" type="button" value="Sign In" variant='dark' size='sm'/>{' '}
            </Nav>   
        </Container>
      </Navbar>
    )
  }

  function NavLogout(props){
    const navigate = useNavigate();
    return(
      <Navbar  bg="dark" variant="dark">
          <Container fluid>
               <Nav>
               <> 
                <Navbar.Brand onClick={() => navigate("/")}>Welcome {props.userPower}</Navbar.Brand>
                {props.userPower === 'localguide' ? 
                <Button onClick={() => navigate("/localguide")}  as="input" type="button" value="Add an hike" variant='dark' size='sm'/> : <></>} 
                <Button onClick={()=> props.logout()} as="input" type="button" value="Logout" variant='dark' size='sm'/>{' '}   
              </>
              </Nav>   
          </Container>
        </Navbar>
      )
  }
  
}

export default MyNavbar2;