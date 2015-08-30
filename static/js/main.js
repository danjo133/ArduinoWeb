
function sendDataSuccess(data) {
    console.log(data);
}

$(document).ready(function(){
    console.log("test logging");

    $('button').click(function() {
	data = {data: $(this).attr("data")};
	$.ajax({
	    url: 'send/' + this.id,
	    type: 'POST',
	    data: JSON.stringify(data,null,'\t'), // An object with the key 'submit' and value 'true;
	    success: sendDataSuccess,
	    contentType: "application/json; charset=utf-8"
	});
    });

});
