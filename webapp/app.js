let get_input_options = function() {
    let minbed = $("select#minbed").val()
    let minbath = $("select#minbath").val()
    let proptype = $("select#proptype").val()
    let neighborhood = $("select#neighborhood").val()
    let maxprice = $("select#maxprice").val()
    return {'minbed': parseInt(minbed),
            'minbath': parseInt(minbath),
            'proptype': proptype.toString(),
            'neighborhood':neighborhood.toString(),
            'maxprice': parseInt(maxprice)}
};

let send_options_json = function(options) {
    $.ajax({
        url: '/solve',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data['table']);
            build_map(data['loc_list'],data['lat_long'])
        },
        data: JSON.stringify(options)
    });
};

let display_solutions = function(solutions) {
    $("table#table").html(solutions)
    let selected_listing = Array.from($("tr")).forEach((el) => {
      const listing_id = $(el).children(':first').text()
      const recommend = () => {
        send_listing_id(listing_id)
      }
      el.addEventListener('click', recommend)
    })
};

let send_listing_id = function(listing_id) {
    $.ajax({
        url: '/recommend',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data['table']);
            build_map(data['loc_list'],data['lat_long'])
        },
        data: listing_id
    });
};

  var locations = [[378740.0, 47.568024, -122.410049],
 [291508.0, 47.605602000000005, -122.28931399999999],
 [463881.0, 47.586418, -122.378464],
 [475306.0, 47.602033, -122.311504],
 [463467.0, 47.508549, -122.265274],
 [477525.0, 47.589806, -122.310578],
 [463849.0, 47.617832, -122.28358500000002],
 [270401.0, 47.605049, -122.336105],
 [472221.0, 47.564236, -122.395798],
 [447339.0, 47.596056, -122.333301],
 [459913.0, 47.604194, -122.30729699999999],
 [455658.0, 47.564701, -122.27111799999999],
 [446156.0, 47.570063, -122.38671399999998],
 [446401.0, 47.58321, -122.39893300000001],
 [426507.0, 47.617278999999996, -122.282234],
 [469006.0, 47.549312, -122.307375],
 [481424.0, 47.638908, -122.388481],
 [381087.0, 47.562094, -122.362885],
 [234555.0, 47.513494, -122.273095],
 [359073.0, 47.595261, -122.31011200000002],
 [279479.0, 47.653605999999996, -122.39093000000001],
 [477888.0, 47.654999, -122.34037],
 [477878.0, 47.651478000000004, -122.331139],
 [478759.0, 47.53223, -122.287865],
 [125133.0, 47.530094, -122.273475],
 [478595.0, 47.67292, -122.354743],
 [480785.0, 47.697832, -122.304847],
 [477812.0, 47.647621, -122.33355700000001],
 [461644.0, 47.617073, -122.35144],
 [221259.0, 47.554404999999996, -122.362549],
 [360156.0, 47.595261, -122.31011200000002],
 [451136.0, 47.629801, -122.34576799999999],
 [460918.0, 47.63345, -122.29900400000001],
 [456211.0, 47.639946, -122.329094],
 [446829.0, 47.566319, -122.36365500000001],
 [476868.0, 47.727275, -122.334602],
 [457871.0, 47.549973, -122.312752],
 [359670.0, 47.587045, -122.30763600000002],
 [477663.0, 47.545891, -122.270103],
 [473651.0, 47.667103000000004, -122.27911399999999],
 [475888.0, 47.601535999999996, -122.333786],
 [477045.0, 47.593193, -122.290901],
 [473070.0, 47.625929, -122.31483700000001],
 [454698.0, 47.609974, -122.32525600000001],
 [39821.0, 47.553643, -122.39894699999999],
 [478960.0, 47.638859000000004, -122.39893300000001],
 [481536.0, 47.598076, -122.30693799999999],
 [452683.0, 47.612988, -122.339302],
 [478178.0, 47.571059999999996, -122.28688799999999],
 [481087.0, 47.628662, -122.350609],
 [476468.0, 47.659248, -122.318497],
 [477136.0, 47.54958, -122.385277],
 [10954.0, 47.531814000000004, -122.277992],
 [480238.0, 47.625735999999996, -122.319473],
 [223763.0, 47.667801000000004, -122.33825700000001],
 [471564.0, 47.530056, -122.28903999999999]]

var lat_lng = {'lat' : 47.6080134, 'lng' : -122.335167}

let build_map = function(locations,lat_lng){
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: new google.maps.LatLng( lat_lng['lat'], lat_lng['lng']),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var infowindow = new google.maps.InfoWindow();

  var marker, i;

  for (i = 0; i < locations.length; i++) {
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(locations[i][1], locations[i][2]),
      url:locations[i][3],
      map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        window.open(this.url) ;
        infowindow.setContent(locations[i][0]);
        infowindow.open(map, marker);
      }
    })(marker, i));
  }
};

$(document).ready(function() {
    build_map(locations,lat_lng)
    $("button#find").click(function() {
        let options = get_input_options();
        send_options_json(options);
    })

})

// $("td").click(function(e) {
//      console.log(e.target.tagName);  });
