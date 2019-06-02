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
    if (feature.properties.FREE == 999)
        var popupContent =  "<b>Id</b>: " + 
                    			feature.properties.BIKE_SH +
                    			"<br><b>Number of stalls</b>: " +
                				feature.properties.STALLI + 
                				"<br><b>Number of bike available</b>: " +
                				"Realtime data not available" + 
                				"<br><b>Number of stalls free</b>: " +
                				"Realtime data not available";
    else
        var popupContent =  "<b>Id</b>: " + 
                    			feature.properties.BIKE_SH +
                    			"<br><b>Number of stalls</b>: " +
                				feature.properties.STALLI + 
                				"<br><b>Number of bike available</b>: " +
                				feature.properties.FREE + 
                				"<br><b>Number of stalls free</b>: " +
                				feature.properties.AVAILABLE
                				;                         				
    layer.bindPopup(popupContent)
}

var stat = L.geoJSON(stalls_free,{
    pointToLayer: function(feature,latlng){
        return L.marker(latlng,{icon: bike_ic})
    },
    onEachFeature: onEachFeature
});

var mymap = L.map('map_premium',{
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

mymap.locate({setView: true, maxZoom: 16});


function onLocationFound(e) {
    var rad = e.accuracy / 2;
    var position = L.circle(e.latlng,{
    color: 'blue',
    fillColor:'blue',
    radius: 1
    }).addTo(mymap);
    L.circle(e.latlng, rad).addTo(mymap);
    var layer = position;
    var nearest = leafletKnn(stat).nearest(e.latlng, 5, 10000*1.61);
    console.log(nearest[0].layer)
    list_station(nearest)                   
}

mymap.on('locationfound', onLocationFound);

function onLocationError(e) {
    alert(e.message);
    $('#nearest_stalls').html(
        "<p>"+ "<b>List of nearest stations</b>: <br><br>" + 
        "You need to allow position to see the nearest stations" + 
        "</p>" 
    )
}

mymap.on('locationerror', onLocationError);

function list_station(l){
    $('#nearest_stalls').html(
        "<p>"+ "<b>List of nearest stations</b>: <br><br>" + 
            l[0].layer._popup._content 
            + "<br><br>"
            + l[1].layer._popup._content 
            + "<br><br>"
            + l[2].layer._popup._content 
            + "<br><br>"
            + l[3].layer._popup._content 
            + "<br><br>"
            + l[4].layer._popup._content +
        "</p>" 
    )
}