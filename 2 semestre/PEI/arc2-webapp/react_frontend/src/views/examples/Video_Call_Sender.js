/*!

=========================================================
* Argon Dashboard React - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-dashboard-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React, { Component } from 'react';
import {Redirect} from "react-router-dom";
import Webcam from "react-webcam";
import Stream from "node-rtsp-stream";

import "./style.css"


import JsmpegPlayer from '../../components/Players/JsmpegPlayer';

// reactstrap components
import {
  Button,
  Card,
  CardHeader,
  CardBody,
  FormGroup,
  Form,
  Input,
  Container,
  Row,
  Col
} from "reactstrap";
// core components
import Header from "../../components/Headers/Header.js";


const videoOptions = {
    poster: 'https://cycjimmy.github.io/staticFiles/images/screenshot/big_buck_bunny_640x360.jpg'
};
  
const videoOverlayOptions = {};

let jsmpegPlayer = null;

class Video_Call_Sender extends Component {

  constructor(props) {
    super(props);
    this.state = {}

  }


  render() {
    return (
      <>
      <Header />
      {/* Page content */}
      <Container className="mt--7" fluid>
        {/* Dark table */}
        <Row className="mt-5">
            
        </Row>
            
      </Container>
      
      </>
      
      
    );
  }

}




export default Video_Call_Sender;
