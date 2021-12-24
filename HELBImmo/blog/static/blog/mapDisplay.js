//displays a openlayers map to element with js-map as id
$(document).ready(function () 
{
    let target = document.getElementById("js-map");

    let iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat([target.getAttribute('longitude'),target.getAttribute('latitude')]))
    });

    let iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
            anchor: [0.5, 1],
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            src: target.getAttribute('data-image'),
        }),
    });

    iconFeature.setStyle(iconStyle);

    let vectorSource = new ol.source.Vector({
        features: [iconFeature],
    });

    let vectorLayer = new ol.layer.Vector({
        source: vectorSource,
    });

    let mapView = new ol.View({
        center: ol.proj.fromLonLat([target.getAttribute('longitude'),target.getAttribute('latitude')]),
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
});