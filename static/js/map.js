mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
const pois = JSON.parse(document.getElementById('pois-data').textContent);

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [pois[0].lon, pois[0].lat],
  zoom: 5
});

pois.forEach(poi => {
  new mapboxgl.Marker()
    .setLngLat([poi.lon, poi.lat])
    .setPopup(new mapboxgl.Popup().setHTML(`<h4>${poi.name}</h4><p>${poi.place_name}</p>`))
    .addTo(map);
});
