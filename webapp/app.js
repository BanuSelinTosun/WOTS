let get_input_coefficients = function() {
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

let send_coefficient_json = function(coefficients) {
    $.ajax({
        url: '/solve',
        contentType: "application/json; charset=utf-8",
        type: 'POST',
        success: function (data) {
            display_solutions(data);
        },
        data: JSON.stringify(coefficients)
    });
};

let display_solutions = function(solutions) {
    $("span#Listings").html(solutions)

};


$(document).ready(function() {

    $("button#find").click(function() {
        let coefficients = get_input_coefficients();
        send_coefficient_json(coefficients);
    })

})
