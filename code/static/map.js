var layer_mapbox_streets = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors,' +
    ' <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibG9yZW56b3N0dWNjaGkiLCJhIjoiY2poOHkxbDV3MDZ6YjMwbzM2M2R1MjYxeiJ9._wsXJw4kbG-02Bhh9EXNQg'
});

var layer_mapbox_satellite = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors,' +
    ' <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.satellite',
    accessToken: 'pk.eyJ1IjoibG9yZW56b3N0dWNjaGkiLCJhIjoiY2poOHkxbDV3MDZ6YjMwbzM2M2R1MjYxeiJ9._wsXJw4kbG-02Bhh9EXNQg'
});

var layer_OSMStandard = L.tileLayer('http://tile.openstreetmap.org/{z}/{x}/{y}.png',{
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors,' +
    ' <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
});

var bike_ic = new L.icon({
    iconUrl: 'static/bike.png',
    iconSize:     [50, 50], 
    iconAnchor:   [25, 50], 
    popupAnchor:  [0, -53]
});

function onEachFeature(feature, layer) {
    var popupContent =                        
                         "<b>Id</b>: " + 
                			feature.properties.BIKE_SH +
                			"<br><b>Number of stalls</b>: " +
            				feature.properties.STALLI ;
    layer.bindPopup(popupContent)
}

var stat = L.geoJSON(stations,{
    pointToLayer: function(feature,latlng){
        return L.marker(latlng,{icon: bike_ic})
    },
    onEachFeature: onEachFeature
});

var mymap = L.map('map',{
    center: [45.47, 9.19],
    zoom: 13,
    minZoom: 12,
    layers: [layer_mapbox_streets, stat]
});

var baseLayers = {
    "OpenStreetMap": layer_OSMStandard,
    "Streets": layer_mapbox_streets,
    "Satellite": layer_mapbox_satellite
};

var overlays = {
    "stations": stat
};

L.control.layers(baseLayers, overlays).addTo(mymap);

L.Control.geocoder({
    collapsed: true,
    position: 'topleft',
    text: 'Search',
    title: 'Testing'
}).addTo(mymap);
