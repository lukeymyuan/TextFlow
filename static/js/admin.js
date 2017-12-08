$(document).ready(function(){

	var endpoint = '/change_db';

	// Have sliders show their values
	$('.slider').change(function(){
		var span_id = '#' + this.id + '-value';
		$(span_id).text(this.value);
	});

	// REDDIT SUBMISSIONS
	$("#submission-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditSubmission',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'RedditSubmission',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-update").click(function(e) {
            var request  = {
                    'command': 'UPDATE',
                    'source': 'RedditSubmission',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-subreddit-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditSubmission',
                    'type': 'SUBREDDIT',
                    'count': $('#subreddit-range').val(),
                    'subreddit': $('#submission-subreddit').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-subreddit-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'RedditSubmission',
                    'type': 'SUBREDDIT',
                    'subreddit': $('#submission-subreddit').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-user-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditSubmission',
                    'type': 'USER',
                    'count': $('#reddit-user-range').val(),
                    'author': $('#submission-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#submission-user-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'RedditSubmission',
                    'type': 'USER',
                    'author': $('#submission-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    // REDDIT COMMENTS
    $("#comment-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditComment',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#comment-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'RedditComment',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#comment-update").click(function(e) {
            var request  = {
                    'command': 'UPDATE',
                    'source': 'RedditComment',
                    'type': 'URL',
                    'url': $('#submission-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });


    $("#comment-subreddit-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditComment',
                    'type': 'SUBREDDIT',
                    'count': $('#reddit-comment-range').val(),
                    'subreddit': $('#comment-subreddit').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#comment-subreddit-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'RedditComment',
                    'type': 'SUBREDDIT',
                    'subreddit': $('#comment-subreddit').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#comment-user-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditComment',
                    'type': 'USER',
                    'count': $('#reddit-comment-user-range').val(),
                    'author': $('#comment-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#comment-user-delete").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'RedditComment',
                    'type': 'USER',
                    'author': $('#comment-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });


    // TWEETS
    $("#tweet-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'Tweet',
                    'type': 'URL',
                    'url': $('#tweet-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Tweet',
                    'type': 'URL',
                    'url': $('#tweet-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-update").click(function(e) {
            var request  = {
                    'command': 'UPDATE',
                    'source': 'Tweet',
                    'type': 'URL',
                    'url': $('#tweet-url').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-hashtag-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'Tweet',
                    'type': 'Hashtag',
                    'count': $('#tweet-hashtag-range').val(),
                    'hashtag': $('#hashtag').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-hashtag-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Tweet',
                    'type': 'Hashtag',
                    'hashtag': $('#hashtag').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-user-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'Tweet',
                    'type': 'USER',
                    'count': $('#twitter-user-range').val(),
                    'author': $('#twitter-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#tweet-user-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Tweet',
                    'type': 'USER',
                    'author': $('#twitter-user').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });


    // BOOKS
    $("#book-id-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'Book',
                    'type': 'ID',
                    'id': $('#book-id').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#book-id-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Book',
                    'type': 'ID',
                    'id': $('#book-id').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#book-title-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Book',
                    'type': 'Title',
                    'title': $('#book-title').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#book-author-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Book',
                    'type': 'Author',
                    'author': $('#book-author').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });


    // GENERIC
    $("#generic-insert").click(function(e) {
            var request  = {
                    'command': 'INSERT',
                    'source': 'Generic',
                    'name': $('#generic-name').val(),
                    'tag': $('#generic-tags').val(),
                    'text': $('#generic-text').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });

    $("#generic-delete").click(function(e) {
            var request  = {
                    'command': 'DELETE',
                    'source': 'Generic',
                    'name': $('#generic-name').val(),
                    'tag': $('#generic-tags').val(),
                    'text': $('#generic-text').val()
            }
            console.log("Making request to server:", request);
            $.post(endpoint, request, function(response){
                    console.log("Recieved response from server:", response);
            });
            return false;
    });



});