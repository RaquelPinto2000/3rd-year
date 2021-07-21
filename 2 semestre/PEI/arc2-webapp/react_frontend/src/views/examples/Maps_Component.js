import React, { useState, useEffect } from "react";
// react plugin used to create google maps
import {GoogleMap, Marker, withGoogleMap, withScriptjs,Polyline, Circle, DirectionsRenderer} from "react-google-maps";
// core components
/* global google */

function MyDirectionsRenderer(props) {
  const [directions, setDirections] = useState(null);
  const { origem, destino, travelMode } = props;

  useEffect(() => {
    const directionsService = new google.maps.DirectionsService();
    directionsService.route(
      {
        origin: new google.maps.LatLng(origem.lat, origem.lng),
        destination: new google.maps.LatLng(destino.lat, destino.lng),
        travelMode: travelMode
      },
      (result, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
          setDirections(result);
        } else {
          console.error(`error fetching directions ${result}`);
        }
      }
    );
  }, [origem]);

  return (
    <React.Fragment>
      
      {directions && <DirectionsRenderer directions={directions} options={{suppressMarkers:true, preserveViewport: true} } /> }

    </React.Fragment>
  );
}

const MapWrapper = withScriptjs(
    withGoogleMap(props => 
    <GoogleMap
            defaultCenter= {props.defaultCenter}
            defaultZoom={props.zoom}
            defaultOptions={{
              scrollwheel: false,
            }}
        >
        {props.markers.map((props,index) =>{

          return(
          <Marker 
            position={{
              lat: props.lat, 
              lng: props.lng
            }}
           key={index}
           id={index}
           options={{icon:`/accident_icon/${props.status}`}}
           onClick={(() => 
            { if(props.id)
                {window.location.href =`/#admin/accident_details/${props.id}`}
              }
              )}
             />
            );
          })}
        </GoogleMap>
    ));


function handleMarkerClick(id_acc, id_target) {
  console.log("Marker clicked!")
  let res = (fetch(`/startStream/${id_acc}/${id_target}`));
}
function handleCenterChanged(){
  console.log("center" + this.getCenter())
  return this.getCenter()

}
function handleZoomChanged(zoom){
  console.log("Zoom: " + this.getZoom()) //this refers to Google Map instance
  /*if(zoom != this.getZoom()){
    zoom=this.getZoom()
    console.log("zoomMudado =" + zoom)
    return this.getZoom()
  }*/
  return this.getZoom()
}
const MapViewDirections_details =  withScriptjs(
withGoogleMap(props => <GoogleMap
        center= {props.center}
        zoom={props.zoom}
        defaultOptions={{
          scrollwheel: false,
        }}

        onCenterChanged={handleCenterChanged}
    >,

      <MyDirectionsRenderer
        destino={props.origem}
        origem={props.destino}
        travelMode={google.maps.TravelMode.DRIVING}
      />

    {props.markers.map((props,index) =>
      <Marker 
      position={{lat: props.lat, lng: props.lng}}
      key={index}
      id={index}
      options={{icon:`/accident_icon/${props.status}`}}
        onClick={(() => 
        { if(props.id){
            if (props.status == 5) {
              {handleMarkerClick(props.id_acc, props.id)}
            }
          }
        }
        )}
          >
        </Marker>
    )}
    
    </GoogleMap>
));

class Maps extends React.Component {

  constructor(props){
    super(props);

    this.state = {
      lat: 0,
      lng: 0
    }
  }

  componentDidMount(){
    Promise.all([this.get_my_location()]).then((value) => {
      this.setState(
        {
          lat: value[0].coords.latitude,
          lng: value[0].coords.longitude
        })})
  }

  get_my_location = () => {
    if (navigator.geolocation) {
      return new Promise(
        (resolve, reject) => navigator.geolocation.getCurrentPosition(resolve, reject)
      )
    } else {
      return new Promise(
        resolve => resolve({})
      )
    }
  }

  render() 
  {
    if (this.props.center)
      return(
        /*<MapWrapper_details
        googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyDcLG_2KgktdQJXLaeyQZHJzmvcSjNwoPM"
        loadingElement={<div style={{ height: `100%` }} />}
        center = {this.props.center}
        zoom = {this.props.zoom}
        markers = {this.props.markers}
        containerElement={
            <div
                className="map-canvas"
                id="map-canvas"
            />
        }
        mapElement={this.props.mapElement}
      />,*/
      <MapViewDirections_details
          googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyA03XhgCxn-V9TsghBLpQ8LaScQLPgIJxs"
          loadingElement={<div style={{ height: `100%` }} />}
          center = {this.props.center}
          //onCenterChanged={handleCenterChanged}
          zoom = {this.props.zoom}
          markers = {this.props.markers}
          origem={this.props.origem}
          destino={this.props.destino}
          containerElement={
              <div
                  className="map-canvas"
                  id="map-canvas"
              />
          }
          mapElement={this.props.mapElement}
        />
    )
    return (
    <MapWrapper
        googleMapURL="https://maps.googleapis.com/maps/api/js?key=AIzaSyA03XhgCxn-V9TsghBLpQ8LaScQLPgIJxs"
        loadingElement={<div style={{ height: `100%` }} />}
        defaultCenter = {this.state}
        zoom = {this.props.zoom}
        markers = {this.props.markers}
        containerElement={
            <div
                className="map-canvas"
                id="map-canvas"
            />
        }
        mapElement={this.props.mapElement}
    />

    );
  }
}

export default Maps;