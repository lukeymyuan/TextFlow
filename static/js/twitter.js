$(document).ready(function(){
    console.log("Loaded JQuery");
    function toggle_examples() {
        var div = document.getElementById('examples');
        var isHidden = false;

        if (div.style.display === "none") {
            div.style.display = "block";
        } else {
            div.style.display = "none";
            isHidden = true;
        }
        return isHidden;
    }
    var prev_examples = [];
    $("#generate").click(function(e){

	// Hide examples
	var div = document.getElementById('examples');
	div.style.display = "none";

	var request  = {
        'source': "Tweet",
	    'author': $("#authorInput").val(),
	    'hashtag': $('#hashtagInput').val(),
	    'time_period': $("#timeSelect").val(),
        'degree': $('#degree').val()
	};

	console.log("Making request to server:", request);

	$.post('/requests', request, function(response){
	    console.log("Recieved response from server:", response);
	    // Display the generated submission
	    if (response['source'] == 'Tweet') {
	    	$("#tweet-body").text(response['text']);
	    	$("#tweet-body").parent().removeAttr('hidden');
		}

	    prev_examples = response['examples'];
	});
	return false;
    });

    $('#showSources').click(function(e){

	var isHidden = toggle_examples();
	if (isHidden) {
	    return;
	}

	// Remove current examples
	var div = $('#examples');
	div.empty();

	// Add new examples
	if (prev_examples.length > 0) {
	    div.append('<hr>');
	    for (var i = 0; i < prev_examples.length; i++) {

    		var example = prev_examples[i];
            var date = new Date(example['time']*1000);
            var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            var month = months[date.getMonth()];
            var day = date.getDate();
            // Hours part from the timestamp
            var hours = date.getHours();
            // Minutes part from the timestamp
            var minutes = "0" + date.getMinutes();

            // Will display time in 10:30:23 format
            var formattedTime = month +" "+ day +"  "+ hours + ':' + minutes.substr(-2);
            div.append("<h3 display: inline; class='.text-dark'>" + example['author']+" • "+formattedTime + "</h3>" );
    		div.append('<p class="text-secondary">' + example['text'] + '</p>');
            div.append('<hr>');
	    }
	}
    });

});
