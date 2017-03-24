let get_input_options = function() {
    let minbed = $("input#minbed").val()
    let maxbed = $("input#maxbed").val()
    let minbath = $("input#minbath").val()
    let maxbath = $("input#maxbath").val()
    let proptype = $("input#proptype").val()
    let neighborhood = $("input#neighborhood").val()
    return {'minbed': parseInt(minbed),
            'maxbed': parseInt(maxbed),
            'minbath': parseInt(minbath),
            'maxbath': parseInt(maxbath),
            'proptype':proptype.toString(),
            'neighborhood': neighborhood.toString()}
};

let send_options_json = function(options) {
    $.ajax({
        url: '/solve',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data[0]);
            build_map(data[1])
        },
        data: JSON.stringify(options)
    });
};

let display_solutions = function(solutions) {
    $("span#Listings").html(solutions)

};


  var locations = [['$819,950', 47.674609999999994, -122.38545900000001],
['$749,950', 47.671803000000004, -122.38584099999999],
['$614,500', 47.675446, -122.39018700000001],
['$529,000', 47.675509000000005, -122.37896],
['$435,000', 47.671391, -122.382706],
['$650,000', 47.670338, -122.391899],
['$730,000', 47.666396999999996, -122.36713200000001],
['$574,990', 47.669304, -122.39373799999998],
['$399,950', 47.665504, -122.369942],
['$495,000', 47.668343, -122.36289199999999],
['$599,999', 47.670627, -122.391494],
['$799,950', 47.673325, -122.383698],
['$589,950', 47.674049, -122.378128]];

let build_map = function(locations){
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    center: new google.maps.LatLng( 47.671280461538458, -122.38169815384616),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  var infowindow = new google.maps.InfoWindow();

  var marker, i;

  for (i = 0; i < locations.length; i++) {
    marker = new google.maps.Marker({
      position: new google.maps.LatLng(locations[i][1], locations[i][2]),
      map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
      return function() {
        infowindow.setContent(locations[i][0]);
        infowindow.open(map, marker);
      }
    })(marker, i));
  }
};

$(document).ready(function() {
    build_map(locations)
    $("button#find").click(function() {
        let options = get_input_options();
        send_options_json(options);
    })

})
