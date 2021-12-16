const target = document.getElementById('map');
const longitude = document.getElementById('id_longitude').value;
const latitude = document.getElementById('id_latitude').value;

const iconFeature = new ol.Feature({
    geometry: new ol.geom.Point(ol.proj.fromLonLat([longitude,latitude])),
    name: 'Null Island'
});

const iconStyle = new ol.style.Style({
    image: new ol.style.Icon({
        anchor: [0.5, 1],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        src: target.getAttribute('data-image'),
    }),
});

iconFeature.setStyle(iconStyle);

const vectorSource = new ol.source.Vector({
    features: [iconFeature],
});

const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
});

/*const rasterLayer = new ol.layer.Tile({
    source: new ol.source.TileJSON({
        url: 'https://a.tiles.mapbox.com/v3/aj.1x1-degrees.json?secure=1',
        crossOrigin: '',
    }),
});*/

const mapView = new ol.View({
    center: ol.proj.fromLonLat([longitude,latitude]),
    zoom: 16
});


var map = new ol.Map({
    target: target,
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        }),
        vectorLayer
    ],
    view: mapView
});

/*const modify = new ol.interaction.Modify({
    hitDetection: vectorLayer,
    source: vectorSource,
});
modify.on(['modifystart', 'modifyend'], function (evt) {
    target.style.cursor = evt.type === 'modifystart' ? 'grabbing' : 'pointer';
});
const overlaySource = modify.getOverlay().getSource();
overlaySource.on(['addfeature', 'removefeature'], function (evt) {
    target.style.cursor = evt.type === 'addfeature' ? 'pointer' : '';
});

map.addInteraction(modify);*/

var geocoder = new Geocoder('nominatim', {
    provider: 'osm',
    key: '',
    lang: 'fr-BE', //en-US, fr-FR
    placeholder: 'Search for ...',
    targetType: 'text-input',
    limit: 3,
    keepOpen: false
});
map.addControl(geocoder);

geocoder.on('addresschosen', function (evt) {
    var feature = evt.feature,
        coord = evt.coordinate,
        address = evt.address;
    iconFeature.setGeometry(new ol.geom.Point(coord));
    // some popup solution
    //overlay.setPosition(coord);
    console.info(evt);
    let addr = address.original.details;
    let city = (addr.city)? addr.city : (addr.town)? addr.town: (addr.village)? addr.village : underfined;
    let state = (addr.state)? addr.state : addr.region;
    let lonlat = ol.proj.toLonLat(coord, 'EPSG:3857');
    let fullAddr = /*address.original.formatted + '|' + */addr.road + ' ' + addr.house_number + '|' + addr.postcode + ' ' + city + ', ' + state + '|' + addr.country_code.toUpperCase() + '|' + lonlat[0] + '|' + lonlat[1];
    document.getElementById('id_address').setAttribute('value', fullAddr);
});