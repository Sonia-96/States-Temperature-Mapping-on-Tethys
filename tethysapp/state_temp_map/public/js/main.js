$(function() {
    let map = TETHYS_MAP_VIEW.getMap();
    console.log("hello");
    console.log(map);
    let geojson_layer;
    map.getLayers().forEach(layer => {
        if (layer.tethys_legend_title == "States Temperature") {
            geojson_layer = layer;
        }
    });
    features = geojson_layer.getSource().getFeatures();
    for (let feature of features) {
        let color = setFeatureColor(feature)
        let style = new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: 'rgba(120, 120, 120, 0.8)',
                lineDash: [10, 10],
                width: 3
            }),
            fill: new ol.style.Fill({
                color: color,
                opacity: 0.3,
            }),
        })
        feature.setStyle(style);
    }
});

function setFeatureColor(feature) {
    let temp = feature.A.AVG_TEMP;
    let temp_value;
    if (temp) {
        temp_value =  parseFloat(temp.split(" ")[0]);
    }
    let opacity = 0.8;
    if (temp_value < 50) {
        return `rgba(33, 102, 172, ${opacity})`;
    }
    if (temp_value < 60) {
        return `rgba(103, 169, 207, ${opacity})`;
    }
    if (temp_value < 70) {
        return `rgba(239, 138, 98, ${opacity})`;
    }
    return `rgba(178, 24, 43, ${opacity})`;

}