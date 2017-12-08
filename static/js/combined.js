
$(document).ready(function(){
    console.log("Loaded JQuery");

    var prev_examples = [];
    subreddits = [];
        
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

    $("#generate").click(function(e){
		// Hide examples
		var div = document.getElementById('examples');
		div.style.display = "none";

		var source = 'Combined';

		var request  = {
		    'source': source,
		    'author': $("#authorInput").val(),
		    'time_period': $("#timeSelect").val(),
	        'degree': $('#degree').val()
		};

		if (request['degree'] == null) {
			request['degree'] = 1
		}

		console.log("Making request to server:", request);

		$.post('/requests', request, function(response){
		    console.log("Recieved response from server:", response);
		    // Display the generated submission
			$("#result-count span").text(response['result_count']);
			$("#result-count").removeAttr('hidden');

		    $("#text").text(response['text']);

	    	$("#text").parent().removeAttr('hidden');
			

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
	    		div.append('<p class="text-secondary">' + example['text'] + '</p>');
	    		div.append('<hr>');
		    }
		}
    });
});
