$(document).ready(function(){
    console.log("Jquery loaded");
    $("#generic-generate").on("click", function(){
		var arrayTags = $('#generic-tags').val().split(",");
		for (index = 0; index <arrayTags.length; index++){
		    arrayTags[index] = arrayTags[index].replace(/[^\w\s]|_/g, "").replace(/^\s+/, "").replace(/\s+$/, "");
		    console.log(arrayTags[index]);
        }
        alert(arrayTags);
	});
});