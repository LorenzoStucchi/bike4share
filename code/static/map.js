var mymap = L.map('map').setView([45.47, 9.19], 13);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors,' +
    ' <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
    'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibG9yZW56b3N0dWNjaGkiLCJhIjoiY2poOHkxbDV3MDZ6YjMwbzM2M2R1MjYxeiJ9._wsXJw4kbG-02Bhh9EXNQg'
}).addTo(mymap);

function onEachFeature(feature, layer) {
    var popupContent =                        
                         "<b>Id</b>: " + 
                			feature.properties.BIKE_SH +
                			"<br><b>Number of stalls</b>: " +
            				feature.properties.STALLI ;
    layer.bindPopup(popupContent)
}

L.geoJSON(stations,{
    onEachFeature: onEachFeature
}).addTo(mymap);