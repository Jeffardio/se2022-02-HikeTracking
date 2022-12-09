import Sidebar from './sidebar';
import { Routes, Route } from 'react-router-dom';
import { Col, Row } from 'react-bootstrap';
import API from '../API';
import { useState, useEffect } from 'react';
//platform manager dont need to show hikes so i just develop the page to confirm accounts



import ConfirmAccount from './confirmAccount';

function PlatformManager(props){
// use effects that need to PM
const [req,setReq] = useState([{mail:"ccc@gmail.com", role:"localguide"}]);
const [errorMessage,setErrorMessage]=useState("")
const [dirty,setDirty]=useState(true)
let token = localStorage.getItem("token");
/*useEffect(() => {
    const getRequests = async () => {
      
        if (dirty) 
        try {
        setDirty(false)
        const requests = await API.getRequests(token);
        if (requests.error)
          setErrorMessage(requests.msg)
        else
          setReq(requests.msg);
      } catch (err) {
        console.log(err)
      }
    }
    getRequests()
  },[dirty]);
  */
    
    

    
    return(
    <>
    <Sidebar userPower={"platformmanager"}/>
    <Col sm={10} className="py-1">
    <Row className="p-4">
    <Routes>
        <Route path="confirmAccount" element={<ConfirmAccount setDirty={setDirty} req={req} />}/>
    </Routes>
    </Row>
    </Col>
    </>
    )
}

export default PlatformManager