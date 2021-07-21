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
import React from "react";
import ImageGallery from 'react-image-gallery';
import "../../assets/css/custom.css"
import JsmpegPlayer from '../../components/Players/JsmpegPlayer';



// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  Container,
  Row,
  Col,
  CardTitle,
  Button,
  UncontrolledCollapse,
  ButtonDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem, Badge
} from "reactstrap";
// core components
import Header from "../../components/Headers/Header.js";
import Maps from "./Maps_Component.js";
import { Redirect } from "react-router-dom";
import UncontrolledAlert from "reactstrap/lib/UncontrolledAlert";
import { isConstructorDeclaration } from "typescript";

const PREFIX_URL = 'https://raw.githubusercontent.com/xiaolin/react-image-gallery/master/static/';
const MEDIA_URL = '/media/'

const videoOptions = {
  poster: './big_buck_bunny_640x360.jpg'
};

const videoOverlayOptions = {};

let jsmpegPlayer = null;

function fix_date(st) {
  let date = st.split('T');
  let year = date[0];
  let time = date[1].split('.')[0];
  return year + " " + time;
}

class AccidentDetails extends React.Component {
  constructor(props) {
    super(props);

    this.timer = null;

    this.toggle = this.toggle.bind(this);
    this.changeValue = this.changeValue.bind(this);

    this.all_locations = [];

    this.state = {
      ambulance: 0,
      user_ambulances: [],
      showIndex: false,
      showBullets: true,
      infinite: true,
      showThumbnails: true,
      showFullscreenButton: true,
      showGalleryFullscreenButton: true,
      showPlayButton: false,
      showGalleryPlayButton: false,
      showNav: true,
      isRTL: false,
      slideDuration: 5,
      slideInterval: 2000,
      slideOnThumbnailOver: false,
      thumbnailPosition: 'left',
      showVideo: {},
      video_total: 0,
      photos_total: 0,
      accident_data: {
        car: [],
        location: {
          address: " ",
          coords: { lat: 40, lng: 30 },
          coords_amb: { lat: 40, lng: 30 },
        },
        damage: 0.0,
        date: " ",
        n_cars_involved: 0,
        n_people_involved: 0,
        n_people_injured: 0,
      },
      live_ports: [],
      dropDownValue: 0,
      dropDownOpen: false,
    };
    this.numImg = 0
    this.images = [
      {
        thumbnail: ``,
        original: ``,
        source: '',
        renderItem: this._renderVideo.bind(this)
      },
      {
        original: ``,
        thumbnail: ``,
        imageSet: [
          {
            srcSet: `${PREFIX_URL}image_set_cropped.jpg`,
            media: '(max-width: 1280px)',
          },
          {
            srcSet: `${PREFIX_URL}image_set_default.jpg`,
            media: '(min-width: 1280px)',
          }
        ]
      },
      {
        original: `${PREFIX_URL}1.jpg`,
        thumbnail: `${PREFIX_URL}1t.jpg`,
        originalClass: 'featured-slide',
        thumbnailClass: 'featured-thumb',
      }
    ]
  }

  //sempre que a pagina é atualizada esta funcao e chamada -> faz pedidos

  get_data = async (id) => {

    let all = await fetch(
      `/list_accidents`);
    let result_all = await all.json();
    let all_locations = [];
    for (let i = 0; i < result_all.length; i++) {
      if (parseInt(result_all[i]["id"]) != parseInt(this.props.match.params['id'])) {
        all_locations.push(
          {
            lat: result_all[i]["location"]["lat"],
            lng: result_all[i]["location"]["lng"],
            id: result_all[i]["id"],
            status: 4
          }
        )
      }
    }
    //carro acidentado
    all_locations.push(
      {
        id: this.props.match.params['id'],
        lat: this.state.accident_data.location.coords.lat,
        lng: this.state.accident_data.location.coords.lng,
        status: this.state.accident_data.status
      }
    )
    //ambulancia
    all_locations.push(
      {
        id: this.props.match.params['id'],
        lat: this.state.accident_data.location.coords_amb.lat,
        lng: this.state.accident_data.location.coords_amb.lng,
        status: 3
      }
    )

    if (this.state.surrounding_cars != undefined) {
      for (let i = 0; i < this.state.surrounding_cars.length; i++) {
        all_locations.push(
          {
            id: this.state.surrounding_cars[i]['car_id'],
            lat: parseFloat(this.state.surrounding_cars[i]['latitude']),
            lng: parseFloat(this.state.surrounding_cars[i]['longitude']),
            id_acc: this.props.match.params['id'],
            status: 5
          }
        )
      }
    }

    if (this.state.surrounding_cameras != undefined) {
      for (let i = 0; i < this.state.surrounding_cameras.length; i++) {
        all_locations.push(
          {
            id: this.state.surrounding_cameras[i]['id'],
            lat: parseFloat(this.state.surrounding_cameras[i]['latitude']),
            lng: parseFloat(this.state.surrounding_cameras[i]['longitude']),
            id_acc: this.props.match.params['id'],
            status: 6
          }
        )
      }
    }

    this.all_locations = all_locations;

    let ports = await (await fetch(`/videos/${id}`)).json();

    let response = await fetch(
      `/markers/${id}`);
    let ress = await response.json();

    let carsResponse = await (await fetch(`/CarsMarkers/${id}`)).json();

    response = await fetch(
      `/accident/${id}`);
    let result = await response.json();

    response = await fetch(
      `/ambulances_by_user`);
    let resultee = await response.json();


    //console.log(this.state.accident_data.location.coords_amb)
    this.setState(prevState => (
      {
        accident_data: {
          car: result['cars'],
          location:
          {
            address: result['location']['address'],
            coords: { lat: result['location']['lat'], lng: result['location']['lng'] },
            coords_amb: { lat: parseFloat(ress["lat"]), lng: parseFloat(ress["lng"]) }
          },
          damage: result['damage'],
          date: fix_date(result['date']),
          n_cars_involved: result['n_cars_involved'],
          n_people_involved: result['n_people'],
          n_people_injured: parseInt(result['n_people_injured']),
          status: result['status']
        },
        live_ports: ports[id],
        surrounding_cars: carsResponse['carData'],
        surrounding_cameras: prevState.surrounding_cameras,
        video_total: parseInt(result['video_total,oca']),
        dropDownValue: this.init_text_dropdown(parseInt(result['status'])),
        user_ambulances: resultee
      }
    ));

    const resp = await fetch(
      `/Nmedia/${id}/photos`);
    const res = await resp.json();
    this.numImg = parseInt(res)
    const media = []
/*     const user_ambs = []
    for(let i = 1; i < resultee.length; i++) {
      user_ambs.push(resultee[i])
    }
    this.user_ambulances = user_ambs
    console.log(this.user_ambulances) */
    if (this.state.video_total > 0) {
      for (let i = 1; i < this.state.video_total + 1; i++) {
        media.push({
          thumbnail: `/media/${id}/video/${i}T.jpg`,
          original: `/media/${id}/video/${i}T.jpg`,
          source: `/media/${id}/video/${i}.mp4`,
          renderItem: this._renderVideo.bind(this)
        })
      }
    } else {
      media.push({
        thumbnail: `/media/novideo.png`,
        original: `/media/novideo.png`
      })
    }
    for (let i = 0; i < this.numImg; i++) {
      media.push({
        thumbnail: `/media/${id}/photos/${i}.jpeg`,
        original: `/media/${id}/photos/${i}.jpeg`
      })
    }

    this.setState(prevState => (
      this.images = media
    ));



  }

  get_cameras = async (id) => {

    let all_locations = this.all_locations;
    let camerasResponse = await (await fetch(`/CameraMarkers/${id}`)).json();

    //console.log(camerasResponse)

    this.setState(prevState => (
      {
        surrounding_cameras: camerasResponse['camData']
      }
    ));

    //console.log(this.state.surrounding_cameras)

    if (this.state.surrounding_cameras != undefined) {
      for (let i = 0; i < this.state.surrounding_cameras.length; i++) {
        all_locations.push(
          {
            id: this.state.surrounding_cameras[i]['id'],
            lat: parseFloat(this.state.surrounding_cameras[i]['latitude']),
            lng: parseFloat(this.state.surrounding_cameras[i]['longitude']),
            id_acc: this.props.match.params['id'],
            status: 6
          }
        )
      }
    }

    this.all_locations = all_locations;
  }

  componentDidMount() {
    let id = this.props.match.params['id']
    this.get_data(id)
    this.get_cameras(id)  // get cameras only once
    this.timer = setInterval(() => this.get_data(id), 1000) //5000

  }

  componentDidUpdate(prevProps, prevState) {
    if (this.state.slideInterval !== prevState.slideInterval ||
      this.state.slideDuration !== prevState.slideDuration) {
      // refresh setInterval
      this._imageGallery.pause();
      this._imageGallery.play();
    };
  }

  componentWillUnmount() {
    clearInterval(this.timer)
    this.timer = null
  }


  renderAlertLives = (value, index) => {

    return (
      <UncontrolledAlert color="success" class="alert">
        <span className="alert-inner--icon">
          <i className="ni ni-like-2" />
        </span>{" "}
        <span className="alert-inner--text">
          <strong>A LIVESTREAM WAS FOUND!</strong>
        </span>
      </UncontrolledAlert>
    )
  }

  renderUserAmbs = (value,index) => {
    var amb = "amb"+String(index)
    return (
      <option value={amb} >{value}</option>
    )
  }

  renderLivestream = (value, index) => {

    let port = String(value['port']).split(':')[2] - 9000;

    if (port < 1000) {
      return (

        <CardBody className="border rounded">
          <CardTitle
            tag="h4"
            className="text-uppercase text-muted mb-0"
          >
            Livestream {index + 1}
          </CardTitle>

          <CardBody className="align-content-center">
            <Row>
              <span className="font-weight-bold">Car id</span>
              <span>: {String(port)}</span>
            </Row>
            <Col width="inherit" height="inherit">
              <Card className="card-stats mb-4 mb-xl-0">
                <CardBody className="border rounded border-info">
                  <Row>
                      <div class="card-body align-items-right">
                        <JsmpegPlayer
                          wrapperClassName="video-wrapper"
                          videoUrl={String(value['port'])}
                          options={videoOptions}
                          overlayOptions={videoOverlayOptions}
                          onRef={ref => jsmpegPlayer = ref}
                        />
                      </div>
                    </Row>
                    <Row>
                      <div className="buttons-wrapper">
                        <Button onClick={() => jsmpegPlayer.play()}>Play</Button>
                        <Button onClick={() => jsmpegPlayer.pause()}>Pause</Button>
                        <Button onClick={() => jsmpegPlayer.stop()}>Stop</Button>
                      </div>
                    </Row>
                </CardBody>
              </Card>
            </Col>
          </CardBody>
        </CardBody>
      )
    } else {
      return (

        <CardBody className="border rounded">
          <CardTitle
            tag="h4"
            className="text-uppercase text-muted mb-0"
          >
            Livestream {index + 1}
          </CardTitle>

          <CardBody className="align-content-center">
            <Row>
              <span className="font-weight-bold">Camera id</span>
              <span>: {String(port)}</span>
            </Row>
            <Col width="inherit" height="inherit">
              <Card className="card-stats mb-4 mb-xl-0">
                <CardBody className="border rounded border-info">
                    <Row>
                      <div class="card-body align-items-right">
                        <JsmpegPlayer
                          wrapperClassName="video-wrapper"
                          videoUrl={String(value['port'])}
                          options={videoOptions}
                          overlayOptions={videoOverlayOptions}
                          onRef={ref => jsmpegPlayer = ref}
                        />
                      </div>
                    </Row>
                    <Row>
                      <div className="buttons-wrapper">
                        <Button onClick={() => jsmpegPlayer.play()}>Play</Button>
                        <Button onClick={() => jsmpegPlayer.pause()}>Pause</Button>
                        <Button onClick={() => jsmpegPlayer.stop()}>Stop</Button>
                      </div>
                    </Row>
                </CardBody>
              </Card>
            </Col>
          </CardBody>
        </CardBody>
      )
    }
  }

  renderCars = (value, index) => {

    return (
      <CardBody className="border rounded">
        <CardTitle
          tag="h4"
          className="text-uppercase text-muted mb-0"
        >
          Car {index + 1}
        </CardTitle>
        <CardBody className="align-content-center">
          <Row>
            <span className="font-weight-bold">Activated ABS</span>
            <span>: {String(value['ABS'])}</span>
          </Row>
          <Row>
            <span className="font-weight-bold">Fired Airbag</span>
            <span>: {String(value['airbag'])}</span>
          </Row>
          <Row>
            <span className="font-weight-bold">Passengers</span>
            <span>: {value['n_people']} </span>
          </Row>
          <Row>
            <span className="font-weight-bold">Overturned</span>
            <span>: {String(value['overturned'])}</span>
          </Row>
          <Row>
            <span className="font-weight-bold">Temperature</span>
            <span>: {value['temperature']}</span>
          </Row>
          <Row>
            <span className="font-weight-bold">Collision velocity</span>
            <span>: {value['velocity']}</span>
          </Row>
        </CardBody>
      </CardBody>
    )
  }

  _onImageClick(event) {
    console.debug('clicked on image', event.target, 'at index', this._imageGallery.getCurrentIndex());
  }

  _onImageLoad(event) {
    console.debug('loaded image', event.target.src);
  }

  _onSlide(index) {
    this._resetVideo();
    console.debug('slid to index', index);
  }

  _onPause(index) {
    console.debug('paused on index', index);
  }

  _onScreenChange(fullScreenElement) {
    console.debug('isFullScreen?', !!fullScreenElement);
  }

  _onPlay(index) {
    console.debug('playing from index', index);
  }

  _resetVideo() {
    this.setState({ showVideo: {} });

    if (this.state.showPlayButton) {
      this.setState({ showGalleryPlayButton: true });
    }

    if (this.state.showFullscreenButton) {
      this.setState({ showGalleryFullscreenButton: true });
    }
  }

  _toggleShowVideo(url) {
    this.state.showVideo[url] = !Boolean(this.state.showVideo[url]);
    this.setState({
      showVideo: this.state.showVideo
    });

    if (this.state.showVideo[url]) {
      if (this.state.showPlayButton) {
        this.setState({ showGalleryPlayButton: false });
      }

      if (this.state.showFullscreenButton) {
        this.setState({ showGalleryFullscreenButton: false });
      }
    }
  }

  _renderVideo(item) {
    return (
      <div>
        {
          this.state.showVideo[item.source] ?
            <div className='video-wrapper'>
              <a
                className='close-video'
                onClick={this._toggleShowVideo.bind(this, item.source)}
              >
              </a>
              <video autoPlay controls>
                // width='100%'
                // height='100%'
                  <source
                  src={item.source}
                  type="video/mp4">

                </source>
                  // frameBorder='0'
                  // allowFullScreen
                </video>
            </div>
            :
            <a onClick={this._toggleShowVideo.bind(this, item.source)}>
              <div className='play-button' />
              <img className='image-gallery-image' src={item.original} />
              {
                item.description &&
                <span
                  className='image-gallery-description'
                  style={{ right: '0', left: 'initial', height: '100%' }}
                >
                  {item.description}
                </span>
              }
            </a>
        }
      </div>
    );
  }

  onGoBack = () => {
    return <Redirect to="/admin/accidents" />
  }

  /* Status dropdown functions */
  toggle() {
    this.setState({ dropDownOpen: !this.state.dropDownOpen });
  }

  changeValue(e) {
    this.updateDBToSelectedStatus(e.currentTarget.textContent)
    this.setState({ dropDownValue: e.currentTarget.textContent })

  }

  getBarColor(damage) {
    if (damage < 30) {
      return "h2 font-weight-bold mb-0 text-success"
    } else if (damage < 45) {
      return "h2 font-weight-bold mb-0 text-teal"
    } else if (damage < 75) {
      return "h2 font-weight-bold mb-0 text-orange"
    } else { return "h2 font-weight-bold mb-0 text-red" }
  }

  setStatusColor() {
    if (this.state.dropDownValue === "Accident resolved") {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-lime" />
        </Badge>
      )
    }
    if (this.state.dropDownValue === "Emergency services are on their way") {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-yellow" />
        </Badge>
      )
    }
    else {
      return (
        <Badge color="" className="badge-dot badge-lg">
          <i className="bg-red" />
        </Badge>
      )
    }
  }

  init_text_dropdown(id) {
    if (id === 2) {
      return ("Accident resolved")
    } else if (id === 1) {
      return ("Emergency services are on their way")
    } else { return ("Accident still not answered") }
  }

  updateDBToSelectedStatus(value) {
    if (value === "Accident resolved") {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 2
        })
      })
    }
    if (value === "Emergency services are on their way") {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 1
        })
      })
    }
    else {
      fetch(`/set_accident_status/${this.props.match.params['id']}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          "status": 0
        })
      })
    }
  }
  handleClick = (e, id, value) => {
    e.preventDefault();
    let new_injured = this.state.accident_data.n_people_injured + value
    if (new_injured >= 0) {
      this.setState(() => (this.state.accident_data.n_people_injured = new_injured))
      this.set_injured(id, new_injured);
    }
  };

  getSelectValue= async () => {
    var selectedValue = document.getElementById("ambs");
    var amb_id = selectedValue.options[selectedValue.selectedIndex].text
    
    await this.myChangeHandler(amb_id)
    
    this.updateDBToSelectedStatus("Emergency services are on their way")
    var id = this.props.match.params['id']
    fetch(`/markers/${id}`, {
      method: "POST",
      cache: "no-cache",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        "ambulance": this.state.ambulance
      })
    }
    ).then(response => {

      return response.json()
    })
      .then(json => {

        this.setState({ ambulance: json[0] })
      })
    
  }
  mySubmitHandler = (e, id) => {
    e.preventDefault();
    alert("You are submitting " + this.state.ambulance);
    //this.init_text_dropdown(1);
    //this.changeValue("Emergency services are on their way");
    this.updateDBToSelectedStatus("Emergency services are on their way")
    fetch(`/markers/${id}`, {
      method: "POST",
      cache: "no-cache",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        "ambulance": this.state.ambulance
      })
    }
    ).then(response => {

      return response.json()
    })
      .then(json => {

        this.setState({ ambulance: json[0] })
      })
  }
  myChangeHandler = (amb_id) => {
    this.setState({ ambulance: amb_id });
  }

  set_injured(id, value) {
    fetch(`/set_accident_injured/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        "injured": `${value}`
      })
    })
  }



  render() {
    return (
      <>
        <Header />
        <Container className=" mt--7" fluid>
          <Row>
            <Col className=" col">
              <Card className=" shadow">
                <CardHeader className=" bg-transparent">
                  <Row>
                    <Col>
                      <div className="d-flex">
                        <Button
                          className="icon icon-shape bg-info text-white rounded-circle shadow"
                          href="/#admin/accidents"
                          onClick={this.onGoBack()}
                        >
                          <i className="fas fa-angle-left" />
                        </Button>
                        <h2 className=" mt-2 ml-4 ">Accident Details</h2>
                      </div>
                    </Col>
                    <Col>
                      <div className="row justify-content-end">
                        <div className="mr-2">
                          {this.setStatusColor()}
                        </div>
                        <div className="mr-2 ">
                          <ButtonDropdown className="dropdown-width" isOpen={this.state.dropDownOpen} toggle={this.toggle}>
                            <DropdownToggle caret>
                              {this.state.dropDownValue}
                            </DropdownToggle>
                            <DropdownMenu right>
                              <DropdownItem onClick={this.changeValue}>Accident still not answered</DropdownItem>
                              <DropdownItem onClick={this.changeValue}>Emergency services are on their way</DropdownItem>
                              <DropdownItem onClick={this.changeValue}>Accident resolved</DropdownItem>
                            </DropdownMenu>
                          </ButtonDropdown>
                        </div>
                      </div>
                    </Col>
                  </Row>
                </CardHeader>
                <CardBody>
                  <Row className="h-75 ">
                    <Col>
                      <Row >
                        <div className="col">
                          <img src={require("../../assets/img/brand/accident_2021.png")} style={{ height: "100%", width: "100%" }} />
                        </div>
                      </Row>
                      <Row>
                        <div className="col">
                          <p><strong>Address:</strong> {this.state.accident_data.location.address}</p>
                        </div>
                      </Row>
                      <Row>
                        <div className="col-sm">
                          <p><strong>Lat:</strong> {this.state.accident_data.location.coords.lat}</p>
                        </div>
                        <div className="col-sm">
                          <p><strong>Lng:</strong> {this.state.accident_data.location.coords.lng}</p>
                        </div>
                      </Row>
                    </Col>
                    <Col>
                      <CardBody>
                        <ImageGallery
                          ref={i => this._imageGallery = i}
                          items={this.images}
                          lazyLoad={false}
                          onClick={this._onImageClick.bind(this)}
                          onImageLoad={this._onImageLoad}
                          onSlide={this._onSlide.bind(this)}
                          onPause={this._onPause.bind(this)}
                          onScreenChange={this._onScreenChange.bind(this)}
                          onPlay={this._onPlay.bind(this)}
                          infinite={this.state.infinite}
                          showBullets={this.state.showBullets}
                          showFullscreenButton={this.state.showFullscreenButton && this.state.showGalleryFullscreenButton}
                          showPlayButton={this.state.showPlayButton && this.state.showGalleryPlayButton}
                          showThumbnails={this.state.showThumbnails}
                          showIndex={this.state.showIndex}
                          showNav={this.state.showNav}
                          isRTL={this.state.isRTL}
                          thumbnailPosition={this.state.thumbnailPosition}
                          slideDuration={parseInt(this.state.slideDuration)}
                          slideInterval={parseInt(this.state.slideInterval)}
                          slideOnThumbnailOver={this.state.slideOnThumbnailOver}
                          additionalClass="app-image-gallery"
                        />
                      </CardBody>
                    </Col>
                  </Row>
                  <Maps

                    markers={this.all_locations}
                    origem={this.state.accident_data.location.coords}
                    destino={this.state.accident_data.location.coords_amb}

                    googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyA03XhgCxn-V9TsghBLpQ8LaScQLPgIJxs"
                    loadingElement={<div style={{ height: `100%` }} />}
                    center={this.state.accident_data.location.coords}
                    //center = {this.state.accident_data.location.coords_amb}
                    zoom={17}

                    containerElement={
                      <div
                        className="map-canvas"
                        id="map-canvas"
                      />
                    }
                    mapElement={
                      <div style={{ height: `100%`, borderRadius: "inherit" }} />
                    }

                  />
                  <CardHeader>
                    <h3> </h3>
                  </CardHeader>
                  {this.state.live_ports.map(this.renderAlertLives)}
                  <Row>

                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0">
                        <CardBody className="border rounded border-info">
                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Number of cars involved
                                  </CardTitle>
                              <span className="h2 font-weight-bold mb-0">{this.state.accident_data.n_cars_involved}</span>
                            </div>
                            <Col className="col-auto">
                              <Button className="icon icon-shape bg-success text-dark rounded-circle shadow" id="toggler">
                                <i className="fas fa-car" />
                              </Button>
                            </Col>
                          </Row>
                        </CardBody>
                      </Card>
                    </Col>
                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0">
                        <CardBody className="border rounded border-info">

                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Number of persons involved
                                  </CardTitle>
                              <span className="h2 font-weight-bold mb-0">
                                {this.state.accident_data.n_people_involved}
                              </span>
                            </div>
                            <Col className="col-auto">
                              <div className="icon icon-shape bg-info text-dark rounded-circle shadow">
                                <i className="fas fa-users" />
                              </div>
                            </Col>
                          </Row>

                        </CardBody>
                      </Card>
                    </Col>
                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0">
                        <CardBody className="border rounded border-info">
                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Number of persons injured
                                </CardTitle>

                              <span className="h2 font-weight-bold mb-0">
                                <Button className=" icon-sm icon-shapesm bg-warning text-dark shadow" onClick={(e) => this.handleClick(e, this.props.match.params['id'], -1)}>
                                  <i className="fas fa-minus" />
                                </Button>
                                {this.state.accident_data.n_people_injured}
                                <Button className=" icon-sm icon-shapesm bg-success text-dark shadow" onClick={(e) => this.handleClick(e, this.props.match.params['id'], 1)}>
                                  <i className="fas fa-plus" />
                                </Button>
                              </span>

                            </div>
                            <Col className="col-auto">
                              <div className="icon icon-shape bg-danger text-dark rounded-circle shadow">
                                <i className="fas fa-user-injured" />
                              </div>
                            </Col>
                          </Row>
                        </CardBody>
                      </Card>
                    </Col>
                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0">
                        <CardBody className="border rounded border-info">
                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Severity of the accident
                                </CardTitle>
                              <span className={this.getBarColor(this.state.accident_data.damage)}>
                                {this.state.accident_data.damage}
                              </span>
                            </div>
                            <Col className="col-auto">
                              <div className="icon icon-shape bg-yellow text-dark rounded-circle shadow">
                                <i className="fas fa-exclamation-triangle" />
                              </div>
                            </Col>
                          </Row>
                        </CardBody>
                      </Card>
                    </Col>
                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0" >
                        <CardBody className="border rounded border-info">
                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Livestreams
                                  </CardTitle>
                              <span className="h2 font-weight-bold mb-0">{this.state.live_ports.length}</span>
                            </div>
                            <Col className="col-auto">
                              <Button className="icon icon-shape bg-success text-dark rounded-circle shadow" id="togglerLives">
                                <i className="fas fa-video" />
                              </Button>
                            </Col>
                          </Row>
                        </CardBody>
                      </Card>
                    </Col>
                    <Col lg="6" xl="3">
                      <Card className="card-stats mb-4 mb-xl-0"  >
                        <CardBody className="border rounded border-info">
                          <Row>
                            <div className="col">
                              <CardTitle
                                tag="h5"
                                className="text-uppercase text-muted mb-0"
                              >
                                Choose an Ambulance
                                </CardTitle>                                  
                            </div>
                            <Col className="col-auto">
                              <select name="ambs" id="ambs" onChange={this.getSelectValue}  class="btn btn-secondary dropdown-toggle" type="button"  data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                              {/*this.renderUserAmbs(this.state.user_ambulances)*/}
                              <option value="amb0" >0</option>
                              {this.state.user_ambulances.map(this.renderUserAmbs)}
                              </select>
                            </Col>

                          </Row>
                        </CardBody>
                      </Card>
                    </Col>
                   
                  </Row>
                  <UncontrolledCollapse toggler="#toggler">
                    <Card>
                      <CardBody>
                        <Row>
                          {this.state.accident_data["car"].map(this.renderCars)}
                        </Row>
                      </CardBody>
                    </Card>
                  </UncontrolledCollapse>
                  <UncontrolledCollapse toggler="#togglerLives">
                    <Card>
                      <CardBody>
                        <Row>
                          {this.state.live_ports.map(this.renderLivestream)}
                        </Row>
                      </CardBody>
                    </Card>
                  </UncontrolledCollapse>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </Container>
      </>
    );
  }
}

export default AccidentDetails;