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
import './style.css'

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
import UserHeader from "../../components/Headers/UserHeader.js";
import Header from "../../components/Headers/Header.js";

import {Redirect} from "react-router-dom";

const webSocket = new WebSocket("ws://127.0.0.1:5000")
webSocket.onmessage = (event) => {
  handleSignallingData(JSON.parse(event.data))
}

let localStream
let peerConn
let username
let isAudio = true
let isVideo = true

function handleSignallingData(data) {
  switch (data.type) {
      case "offer":
          peerConn.setRemoteDescription(data.offer)
          createAndSendAnswer()
          break
      case "candidate":
          peerConn.addIceCandidate(data.candidate)
  }
}

function createAndSendAnswer () {
  peerConn.createAnswer((answer) => {
      peerConn.setLocalDescription(answer)
      sendData({
          type: "send_answer",
          answer: answer
      })
  }, error => {
      console.log(error)
  })
}

function sendData(data) {
  data.username = username
  webSocket.send(JSON.stringify(data))
}



function joinCall() {

  username = document.getElementById("username-input").value

  document.getElementById("video-call-div")
  .style.display = "inline"

  navigator.getUserMedia({
      video: {
          frameRate: 24,
          width: {
              min: 480, ideal: 720, max: 1280
          },
          aspectRatio: 1.33333
      },
      audio: true
  }, (stream) => {
      localStream = stream
      document.getElementById("local-video").srcObject = localStream

      let configuration = {
          iceServers: [
              {
                  "urls": ["stun:stun.l.google.com:19302", 
                  "stun:stun1.l.google.com:19302", 
                  "stun:stun2.l.google.com:19302"]
              }
          ]
      }

      peerConn = new RTCPeerConnection(configuration)
      peerConn.addStream(localStream)

      peerConn.onaddstream = (e) => {
          document.getElementById("remote-video")
          .srcObject = e.stream
      }

      peerConn.onicecandidate = ((e) => {
          if (e.candidate == null)
              return
          
          sendData({
              type: "send_candidate",
              candidate: e.candidate
          })
      })

      sendData({
          type: "join_call"
      })

  }, (error) => {
      console.log(error)
  })
}


function muteAudio() {
  isAudio = !isAudio
  localStream.getAudioTracks()[0].enabled = isAudio
}


function muteVideo() {
  isVideo = !isVideo
  localStream.getVideoTracks()[0].enabled = isVideo
}


class Video_Call_Receiver extends Component {
  constructor(props) {
    super(props);
    this.state ={}
  }

  


  render() {
    return (
      <>
      <Header />
        <div className="Video_Call_Receiver" >
            <Input placeholder="Enter username..."
                type="text"
                id="username-input" text-align="center" />
            <Button onclick={joinCall}>Join Call</Button>
            <div id="video-call-div">
                <video muted id="local-video" autoplay></video>
                <video id="remote-video" autoplay></video>
                <div class="call-action-div">
                    <Button onclick={muteVideo}>Mute Video</Button>
                    <Button onclick={muteAudio}>Mute Audio</Button>
                </div>
            </div>
        </div>
      </>
    );
  
  }
}

export default Video_Call_Receiver;
