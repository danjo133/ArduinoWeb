// Just write a little debug data from the action
function sendDataSuccess(elem) {
    return function(data) {
	console.log(elem + " successfully sent some data and got this response: " + data);
    }
}
function sendDataFailure(elem) {
    return function(data) {
	console.log(elem + " failed to send some data and got this response: " + data);
    }
}

function getDataSuccess(elem) {
    return function(data) {
	var json = JSON.parse(data);
	console.log(json);
	$.each(json["data"], function (item) {
	    $(elem).append("<li>" + json["data"][item] + "</li>");
	});
    }
}

$(document).ready(function(){
    console.log("test logging");

    // Handle all button control switches on the page
    // They will make a post-request to <url>/send/<data-sensor-id>
    $('.controlswitch').click(function() {
	var id = $(this).attr("data-sensor-id");
	var data = {data: $(this).attr("data-sensor-value")};
	console.log(id);
	console.log(data);

	$.ajax({
	    url: 'send/' + id,
	    type: 'POST',
	    data: JSON.stringify(data, null, '\t'),
	    success: sendDataSuccess(this),
	    failure: sendDataFailure(this),
	    contentType: "application/json; charset=utf-8"
	});
    });

    // Send a request for the available sensor log for the sensor id provided
    $('.sensorlog').each(function(){
	var id = $(this).attr("data-sensor-id");

	if (id) {
	    $.ajax({
		url: 'get/' + id,
		type: 'GET',
		success: getDataSuccess(this),
		contentType: "application/json; charset=utf-8"
	    });
	} else {
	    console.log("Error, no id specified");
	}
    });
});
