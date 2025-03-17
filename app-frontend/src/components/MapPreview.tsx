"use client";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface Position {
  lat: number;
  lng: number;
}

const MapShow = (position: Position) => {
  // Create a custom icon class (preferred method)
  const DefaultIcon = L.icon({
    iconUrl: new URL("leaflet/dist/images/marker-icon.png", import.meta.url)
      .href,
    iconRetinaUrl: new URL(
      "leaflet/dist/images/marker-icon-2x.png",
      import.meta.url
    ).href,
    shadowUrl: new URL("leaflet/dist/images/marker-shadow.png", import.meta.url)
      .href,
    iconSize: [25, 41], // Size of the icon
    iconAnchor: [12, 41], // Point from which the icon is "anchored" to the map
    popupAnchor: [0, -41], // Point from which the popup is anchored relative to the icon
  });

  L.Marker.prototype.options.icon = DefaultIcon; // Apply to all markers

  console.log(position.lat);
  console.log(position.lng);
  return (
    <MapContainer
      center={[position.lat, position.lng]}
      zoom={13}
      scrollWheelZoom
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[position.lat, position.lng]}>
        <Popup>
          {position.lat}, {position.lng}
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default MapShow;
