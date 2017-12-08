console.log("Loaded test.js file");
$(document).ready(function(){
	console.log("Loaded JQuery");

	
	$("#insert").click(function(e) {
		var url = $('#url').val()
		var request  = {
			'command': 'INSERT',
			'url': url
		}
		console.log("Making request to server:", request);

		$.post('/change_db', request, function(response){
			console.log("Recieved response from server:", response);
		});
		return false;
	});

	$("#update").click(function(e) {
                var url = $('#url').val()
                var request  = {
                        'command': 'UPDATE',
                        'url': url
                }
                console.log("Making request to server:", request);

                $.post('/change_db', request, function(response){
                        console.log("Recieved response from server:", response);
                });
                return false;
        });

	$("#delete").click(function(e) {
                var url = $('#url').val()
                var request  = {
                        'command': 'DELETE',
                        'url': url
                }
                console.log("Making request to server:", request);

                $.post('/change_db', request, function(response){
                        console.log("Recieved response from server:", response);
                });
                return false;
        });

	$("#scrape-subreddit").click(function(e) {
                var subreddit = $('#subreddit').val()
                var request  = {
                        'command': 'SCRAPE SUBREDDIT',
                        'subreddit': subreddit
                }
                console.log("Making request to server:", request);

                $.post('/change_db', request, function(response){
                        console.log("Recieved response from server:", response);
                });
                return false;
        });

	$("#delete-subreddit").click(function(e) {
                var subreddit = $('#subreddit').val()
                var request  = {
                        'command': 'DELETE SUBREDDIT',
                        'subreddit': subreddit
                }
                console.log("Making request to server:", request);

                $.post('/change_db', request, function(response){
                        console.log("Recieved response from server:", response);
                });
                return false;
        });

});
