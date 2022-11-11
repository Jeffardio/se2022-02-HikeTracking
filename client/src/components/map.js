import { MapContainer, TileLayer, useMap, Marker, Popup, useMapEvents, Polyline } from 'react-leaflet'
import { useEffect, useState } from 'react'
import { Icon } from 'leaflet'
import GpxParser from 'gpxparser';

const myIconSp = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});


const myIconEp = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

const myIconRp = new Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-yellow.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [20, 35],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function Map(props){
    const [positions, setPositions] = useState([])
    
    const rpList = props.rpList.map((pos) => {
        console.log(pos)
        return <Marker position={[pos['reference_point_lat'],pos['reference_point_lng']]} icon={myIconRp}>
            <Popup>
                Reference Point: {pos['reference_point_address']}
            </Popup>
        </Marker>
    })

    let spMarker = null
    if(props.sp[0]!=='' && props.sp[1]!=='')
        spMarker =(<Marker position={props.sp} icon={myIconSp} >
        <Popup>
            Start point: {props.spAddress}
        </Popup>
        </Marker>)
    let epMarker = null
    if(props.ep[0]!=='' && props.ep[1]!=='')
        epMarker =(<Marker position={props.ep} icon={myIconEp} >
        <Popup>
            End point: {props.epAddress}
        </Popup>
        </Marker>)
    useEffect(() => {
        if (props.gpxFile !== ''){ 
            const gpx = new GpxParser()
            gpx.parse(props.gpxFile)
            let pos = gpx.tracks[0].points.map(p => [p.lat, p.lon])
            setPositions(pos)
        }
    },[props.gpxFile])
    
    

    return (
        <MapContainer center={props.sp} zoom={13} scrollWheelZoom={false} style={{height: '400px'}} onClick={(e) => console.log(e) }>
            <Click sp={props.sp}></Click>
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {spMarker}
            {epMarker}
            {rpList}
            <Polyline
                pathOptions={{ fillColor: 'red', color: 'blue' }}
                positions={
                positions
            }
            />
        </MapContainer>
    )
}

function Click(props){
    const [position, setPosition] = useState([0,0])
    const map = useMapEvents({
        click: (e) => {
            map.flyTo(props.sp)
        },
        
      })
      return null
}
export default Map