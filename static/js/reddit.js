var svgContainer;
class Node{
    constructor(label, probability, x, y){
	this.label = label;
	this.probability = probability;
	this.element = svgContainer.append("g").attr("transform","translate("+x+","+y+")");
	this.scale = 1;
	this.x = x;
	this.y = y;
	this.r = 50;
	this.circle=this.element.append("circle").attr("fill","#fff6fd").attr("r",50);
	this.text = this.element.append("text").text(label).attr("text-anchor","middle");
	this.ptext = this.element.append("text").text(probability).attr("text-anchor","middle").attr("y","1.5em");
    }
    setPosition(x,y){
	this.x = x;
	this.y = y;
	this.element.attr("transform","scale("+this.scale+") translate("+x+","+y+")");
    }
    setRadius(r){
	this.r = r;
	this.circle.attr("r",r);
    }
    setOutline(color){
	this.strokeColor = color;
	this.circle.attr("stroke",color);
    }
    setFill(color){
	this.circle.attr("fill",color);
    }
    pulse(magnitude){
	this.circle.transition().attr("r",this.r*magnitude).attr("stroke","yellow").duration(200);
	this.circle.transition().delay(200).attr("r",this.r).attr("stroke",this.strokeColor).duration(150);
    }

}
//Expected input format: [(word, probability)...]
function createNodes(input){
    var offset = 20;
    var radius = 50;
    var nodes = [];
    input.forEach(function(word,probability, list, index){
	console.log(index);
	var node = new Node(word, probability, 55, offset*index+radius*(2*index+1))
	nodes.push(node);
    });
    return nodes;

}
input = [("hello",.5),("world",.5)]
console.log("Loaded reddit.js file");
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}
var testNode;
$(document).ready(function(){
    console.log("Loaded JQuery");
    svgContainer = d3.select("#svgContainer");
    //var circle = svgContainer.append("circle").attr("cx",30).attr("cy",30).attr("r",20);
    testNode = new Node("Test",.5, 55,55);
    testNode.setOutline("#89a6d4");
    var prev_examples = []
    subreddits = [];
    $.get('/autocomplete',{'table': 'RedditSubmission', 'field':'subreddit'}, function(response){
	console.log(response);
	$("#subredditInput").autocomplete({
	    source: response
	});
    });
    $("#subredditInput").blur(function(){
	$.get('/autocomplete',{'table': 'RedditSubmission', 'field':'author', 'constraint':"subreddit = '{0}'".format($("#subredditInput").val()) }, function(response){
	    $("#authorInput").autocomplete({
		source: response
	    });
	});
    });
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

	var source = $("#sourceSelect").val();

	var request  = {
	    'source': source,
	    'author': $("#authorInput").val(),
	    'subreddit': $('#subredditInput').val(),
	    'time_period': $("#timeSelect").val(),
        'degree': $('#degree').val()
	};

	console.log("Making request to server:", request);

	$.post('/requests', request, function(response){
	    console.log("Recieved response from server:", response);
	    // Display the generated submission
		$("#result-count span").text(response['result_count']);
		$("#result-count").removeAttr('hidden');
	    if (response['source'] == 'RedditSubmission') {
	    	$("#submission-title").text(response['title']);
	    	$("#submission-url").text(response['url']);
	    	$("#submission-selftext").text(response['selftext']);

	    	$("#submission-title").parent().removeAttr('hidden');
            $("#submission-url").parent().removeAttr('hidden');
            $("#submission-selftext").parent().removeAttr('hidden');
		}
		else {
			$("#submission-selftext").text(response['text']);
			$("#submission-selftext").parent().removeAttr('hidden');
			$("#submission-title").parent().attr('hidden');
			$("#submission-url").parent().attr('hidden');
		}

	    prev_examples = response['examples'];
	});
	return false;
    });



    $('#show-sources').click(function(e){

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
            div.append("<h3 class='text-primary'><a href='" + example['url'] + "'</a>" + example['title'] + "</h3>");
    		div.append('<p class="text-secondary"><b>Found in Subreddit: </b>' + example['subreddit'] + '<b> By </b>' + example['author'] + '</p>');
    		div.append('<p class="text-secondary"><b>Score: </b>' + example['score'] + '</p>');
    		//div.append('<p><b>URL: </b>' + example['url'] + '</p>');
    		div.append("<p style='display:none;' id='p" + i + "'>" + example['selftext'] + "</p>");
            div.append("<button class='btn btn-outline-info btn-sm' id='button" + i + "'>Toggle</button>");
            div.append("<script>$(document).ready(function(){ $('#button"+i+"').click(function(){$('#p"+i+"').toggle();   });    });</script>");
    		div.append('<hr>');
	    }
	}
    })

});
