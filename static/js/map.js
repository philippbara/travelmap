mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;

// Parse the full FeatureCollection
const mapData = JSON.parse(document.getElementById('pois-data').textContent);
const features = mapData.features;

// Center the map on the first POI with geometry, fallback if none
const firstFeature = features.find(f => f.geometry && f.geometry.coordinates.length === 2);
const center = firstFeature ? firstFeature.geometry.coordinates : [0, 0];

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: center,
  zoom: 5
});

// Add a marker for each feature that has geometry
features.forEach(feature => {
  if (!feature.geometry || !feature.geometry.coordinates) return;

  const coords = feature.geometry.coordinates;
  const props = feature.properties;

  new mapboxgl.Marker()
    .setLngLat(coords)
    .setPopup(new mapboxgl.Popup().setHTML(`
      <h4>${props.name}</h4>
      <p>${props.description}</p>
      <a href="${props.link}" target="_blank">View on blog</a>
    `))
    .addTo(map);
});
