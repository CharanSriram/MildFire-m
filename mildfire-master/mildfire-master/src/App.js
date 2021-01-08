import React, {useState} from 'react';
import './App.css';
import Navbar from './NavBar/Navbar'
import Alert from './Alert/Alert'
import { GoogleMap, HeatmapLayer, LoadScript, Marker } from '@react-google-maps/api'
import { v4 as uuidv4 } from 'uuid';
import Loadable from "@loadable/component"

export default function App() {

  const [map, setMap] = useState(null)
  const [shouldMark, setMarkerState] = useState(false)
  const [markers, addMarker] = useState([])
  const [heatPoints, addHeatPoints] = useState([])
  let ref;

  function resetMap() {
    navigator.geolocation.getCurrentPosition(function(location) {
        map.panTo({lat: location.coords.latitude, lng: location.coords.longitude})
    })
  }

  function placeMarker(e) {
    if (shouldMark) {
      let current = [...markers]
      current.push(<Marker key={uuidv4()} position={e.latLng}/>)
      addMarker(current)
      getHeatMapPoints(e.latLng.lat(), e.latLng.lng())
      setMarkerState(false)
      resetMap()
    }
  }

  function getHeatMapPoints(lat, lng) {
    fetch(`http://us-central1-mildfire.cloudfunctions.net/testfunction?lat=${lat}&lng=${lng}`)
      .then(res => res.json())
      .then((result) => {
        let currentHeatPoints = [...heatPoints]
        console.log(result)
        result.trees.forEach(arr => {
          console.log(arr[0])
          currentHeatPoints.push(new window.google.maps.LatLngBounds(arr[0], arr[1]))
        })
        addHeatPoints(currentHeatPoints)
        console.log(currentHeatPoints[0])
      })
  }

  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds();
    map.fitBounds(bounds);
    setMap(map)
  }, [])

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null)
  }, [])

    const containerStyle = {
      width: '100%',
      height: '100vh'
    }
    const center = {
      lat: -3.745,
      lng: -38.523
    };


    return (
      <LoadScript libraries={["visualization"]} googleMapsApiKey="AIzaSyAkmEgch9O3C7vpzKXooUM3hiMToGne2oQ">
        <Navbar reset={() => resetMap()}></Navbar>
        <Alert reset={() => resetMap()} changeMarkerState={(b) => setMarkerState(b)}></Alert>
        <GoogleMap 
        onClick={(e) => placeMarker(e)} 
        onLoad={onLoad}
        onUnmount={onUnmount}
        options={{
          streetViewControl: false,
          scaleControl: false,
          mapTypeControl: false,
          panControl: false,
          zoomControl: false,
          rotateControl: false,
          fullscreenControl: false
        }} 
          disableDefaultUI center={center} zoom={17} mapContainerStyle={containerStyle}>
            {map && heatPoints[0] ? <HeatmapLayer data={[heatPoints]} /> : null}
            {markers}
        </GoogleMap>
      </LoadScript>
    )
}

