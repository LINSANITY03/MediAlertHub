import { useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

interface Position {
  lat: number;
  lng: number;
}

interface MapSelectorProps {
    onPositionSelect: (position: Position) => void;
    defaultPosition?: Position; // Make defaultPosition optional
}

// Create a custom icon class (preferred method)
const DefaultIcon = L.icon({
    iconUrl: new URL('leaflet/dist/images/marker-icon.png', import.meta.url).href,
    iconRetinaUrl: new URL('leaflet/dist/images/marker-icon-2x.png', import.meta.url).href,
    shadowUrl: new URL('leaflet/dist/images/marker-shadow.png', import.meta.url).href,
    iconSize: [25, 41], // Size of the icon
    iconAnchor: [12, 41], // Point from which the icon is "anchored" to the map
    popupAnchor: [0, -41] // Point from which the popup is anchored relative to the icon
  });
  
L.Marker.prototype.options.icon = DefaultIcon; // Apply to all markers
  
const MapSelector = (props: MapSelectorProps) => {  
  const { onPositionSelect } = props; // Destructure props
  const initialPosition: Position = props.defaultPosition || { lat: 27.658354, lng: 85.325065 }; // Satdobato location
  const [position, setPosition] = useState<Position>(initialPosition);
  
  const LocationMarker = () => {
    const map = useMapEvents({
      click: (e: L.LeafletMouseEvent) => { 
        const clickedPosition: Position = { lat: e.latlng.lat, lng: e.latlng.lng };
        setPosition(clickedPosition);
        onPositionSelect(clickedPosition);
      },
    });

    return position ? (
      <Marker position={[position.lat, position.lng]}>
        <Popup>You selected this position.</Popup>
      </Marker>
    ) : null;
  };

  return (
    <MapContainer
      center={[initialPosition.lat, initialPosition.lng]}
      zoom={13}
      scrollWheelZoom
      style={{ height: '400px', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <LocationMarker />
    </MapContainer>
  );
};

export default MapSelector;