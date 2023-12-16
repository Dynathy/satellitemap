// Initialize the Cesium Viewer in the div with the ID 'cesiumContainer'.
var viewer = new Cesium.Viewer('cesiumContainer', {
	imageryProvider: new Cesium.SingleTileImageryProvider({
        url: './img/background.png'
    }),
    // Add Cesium viewer options here
	baseLayerPicker: false,
    timeline: false,
    animation: false,
    baseLayerPicker: false,
    fullscreenButton: false,
    homeButton: false,
    geocoder: false,
    navigationHelpButton: false,
	skyBox: false,
    creditContainer: undefined
    // ... other options ...
});

var geoJsonOptions = {
    stroke: Cesium.Color.BLACK,
    fill: Cesium.Color.TRANSPARENT,
    strokeWidth: 2
};

var handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
handler.setInputAction(function(movement) {
    var pickedObject = viewer.scene.pick(movement.endPosition);
    if (Cesium.defined(pickedObject) && pickedObject.id && pickedObject.id.label) {
        pickedObject.id.label.show = true;  // Show label only if it exists
    } else {
        viewer.entities.values.forEach(function(entity) {
            if (entity.label) {
                entity.label.show = false;  // Hide other labels
            }
        });
    }
}, Cesium.ScreenSpaceEventType.MOUSE_MOVE);

// Function to add a satellite to the Cesium Viewer 
function addSatellite(name, lat, lon, alt) {
    var satelliteEntity = viewer.entities.add({
        name: name,
        position: Cesium.Cartesian3.fromDegrees(lon, lat, alt),
        point: {
            pixelSize: 5,
            color: Cesium.Color.BLUE
        },
        label: {
            text: name,
            font: '14pt monospace',
            style: Cesium.LabelStyle.FILL,
            outlineWidth: 2,
            verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
            pixelOffset: new Cesium.Cartesian2(0, -9)
        }
    });

    return satelliteEntity;
}

// Function to fetch satellite data from the Flask server
function fetchSatelliteData() {
    fetch('http://localhost:5000/get_satellite_data')
        .then(response => response.json())
        .then(data => {
            data.slice(0, 5).forEach(sat => {
                
                addSatellite(sat.name, sat.latitude, sat.longitude, sat.altitude);
                drawSatellitePath(sat.path);
            });
        })
        .catch(error => console.error('Error fetching satellite data:', error));
}

function drawSatellitePath(path) {
    // Flatten the array of [lon, lat, alt] arrays into a single array
    var flatPath = path.flat();
	console.log("Drawing path:", flatPath);
    viewer.entities.add({
        polyline: {
            positions: Cesium.Cartesian3.fromDegreesArrayHeights(flatPath),
            width: 1,
            material: Cesium.Color.YELLOW
        }
    });
}

viewer.dataSources.add(Cesium.GeoJsonDataSource.load('./img/worldGeoJSON.geojson',  {
    stroke: Cesium.Color.GREY,
    fill: Cesium.Color.TRANSPARENT,
    strokeWidth: 2
}));

viewer.scene.globe.enableLighting = false;
viewer.scene.globe.baseColor = Cesium.Color.TRANSPARENT;
viewer.scene.skyAtmosphere.show = false;
viewer.scene.globe.showGroundAtmosphere = false;
//viewer.scene.globe.show = false;
// Call the function to fetch and display the satellite data
fetchSatelliteData();
