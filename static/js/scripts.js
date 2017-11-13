console.log("js file loaded");
$(document).ready(function(){
    console.log("Jquery loaded");
    $("#generate").click(function(e){

	query = {
	    'source': $("#sourceSelect").val(),
	    'author': $("#authorInput").val(),
	    'time':   $("#timeInput").val(),
	    'length': $("#lengthInput").val()
	}
	$.post('/query_db', query, function(response){console.log(response);});
	return false;
    });

});
