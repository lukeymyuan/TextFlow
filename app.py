from flask import Flask, render_template, url_for, redirect, request, jsonify
import db
import os.path
import markov
import time
import generator
from scrapers.twitter_scraper import TwitterScraper
from scrapers.reddit_scraper import RedditScraper
app = Flask(__name__)

"""
Below two functions salt the javascript and css files so that the server never uses a cached version.
"""
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route("/")
def home():
        data = db.execute("SELECT * from document")
	return render_template("index.html", data=data)

@app.route("/twitter")
def twitter():
	return render_template("twitter.html")

@app.route("/books")
def books():
	return render_template("books.html")

@app.route("/reddit")
def reddit():
	return render_template("reddit.html")

@app.route("/custom")
def custom():
	return render_template("custom.html")

@app.route("/generic")
def generic():
	return render_template("generic.html")

@app.route("/combined")
def combined():
	return render_template("combined.html")

@app.route("/admin")
def admin():
	return render_template("admin.html")

@app.route("/test")
def test():
	return render_template("test.html")

SOURCES = ["*", "Books", "Papers", "Twitter", "Facebook", "RedditSubmission"]
@app.route("/query_db", methods=["POST"])
def handle_query():
    print(request.form)
    #source = SOURCES[int(request.form['source'])]
    source = "RedditSubmission"
    author = request.form['author']
    length = request.form['length']
    subreddit = "askreddit"
    if length:
        length = int(length)
    else:
        length = 500
    filters = []
    if author != '':
        filters.append('author="{0}"'.format(author))
    if subreddit != '':
        filters.append('UPPER(subreddit)=UPPER("{0}")'.format(subreddit))
    query = """
    SELECT text, url, title FROM {0}
    """.format(source)
    if filters:
        query+="WHERE "+",".join(filters)
    print(query)

    result = db.execute(query)
    texts, urls, titles = zip(*result)

    print(len(result))
    generated_text = markov.generate(" ".join(titles),length)

    return jsonify(generated_text)

@app.route("/autocomplete")
def autocomplete():
    args = request.args
    table = args['table']
    field = args['field']
    query = 'SELECT DISTINCT {0} from {1}'.format(field, table)
    if 'constraint' in args.keys():
        query+= " WHERE " + args['constraint']
    print(query)
    return jsonify([result[0] for result in db.execute(query) if result[0]])

@app.route("/requests", methods=["POST"])
def handle_request():

	# Store when we started processing the request
	start_time = time.time()

	# Put the posted data into a dictionary
	keys = request.form.keys()
	data = dict()
	for key in keys:
		data[key] = request.form[key]

	source = data['source']

	response = dict()

	if source == 'RedditSubmission':
		response = generator.generate_reddit_submission(data)
	elif source == 'RedditComment':
		response = generator.generate_reddit_comment(data)
	elif source == 'Tweet':
		response = generator.generate_tweet(data)
	elif source == 'Book':
		response = generator.generate_book(data)
	elif source == 'Custom':
		response = generator.generate_custom(data)
	elif source == 'Combined':
		response = generator.generate_combined(data)
	else:
		print("WARNING: Unknown source '{0}' given in request.".format(source))

	# Get the total server time it took to process this request
	server_time = time.time() - start_time
	response['server_time'] = server_time
	response['source'] = source
	return jsonify(response)


@app.route("/change_db", methods=["POST"])
def handle_change():
	command = request.form['command']
	source = request.form['source']
	t = request.form['type']
	if command == 'INSERT':
		if source == "RedditSubmission":
			if t == 'URL':
				scraper = RedditScraper(data_path='./scrapers/data/reddit')
				submission = scraper.scrape_submission_from_url(request.form['url'])
				submission = scraper.format_submission(submission)
				db.insert_reddit_submission(submission)
				db.commit()
				return "Inserted Submission"
			elif t == 'SUBREDDIT':
				db.scrape_reddit_submissions(amount=request.form['count'], subreddit=request.form['subreddit'])
				db.commit()
				return "Finished Scraping Subreddit"
			elif t == 'USER':
				db.scrape_reddit_submissions(amount=request.form['count'], user=request.form['user'])
				db.commit()
				return "Finished Scraping User"
		elif source == "RedditComment":
			if t == 'URL':
				scraper = RedditScraper(data_path='./scrapers/data/reddit')
				comment = scraper.scrape_comment_from_url(request.form['url'])
				comment = scraper.format_comment(comment)
				db.insert_reddit_comment(comment)
				db.commit()
				return "Inserted Comment"
			elif t == 'SUBREDDIT':
				db.scrape_reddit_comments(amount=request.form['count'], subreddit=request.form['subreddit'])
				db.commit()
				return "Finished Scraping Subreddit"
			elif t == 'USER':
				db.scrape_reddit_comments(amount=request.form['count'], user=request.form['user'])
				db.commit()
				return "Finished Scraping User"
		elif source == "Tweet":
			if t == "URL":
				scraper = TwitterScraper(data_path='./scrapers/data/twitter')
				return "//TODO"
			elif t.lower() == "hashtag":
				db.scrape_twitter_hashtag(request.form['hashtag'], amount = request.form['count'])
				return "Finished Scraping HashTag"
			elif t == "USER":
				db.scrape_twitter_user(request.form['author'], amount = request.form['count'])
				return "Finished Scraping User"	
	elif command == 'DELETE':
		if source == 'RedditSubmission':
			if t == 'SUBREDDIT':
				db.delete_reddit_submission(subreddit=request.form['subreddit'])
				return "Done"
			elif t == 'USER':
				db.delete_reddit_submission(author=request.form['author'])
				return "Done"	

		return "Done"
	elif command == 'UPDATE':
		scraper = RedditScraper(data_path='./scrapers/data')
                submission = scraper.scrape_submission_from_url(request.form['url'])
		submission = scraper.format_submission(submission)
                db.update_reddit_post(submission)
		db.commit()
                return jsonify(submission)
	elif command == 'SCRAPE SUBREDDIT':
                scraper = RedditScraper(data_path='./scrapers/data')
		subreddit = request.form['subreddit'].lower()
                new_data = scraper.scrape_subreddit(subreddit=subreddit, submissions=100, comment_submissions=0, comments_per_sub=0, time_period='year')

		if len(new_data['submissions']) > 0:
			for submission in new_data['submissions']:
				db.insert_reddit_post(submission)
                	db.commit()
		#if len(new_data['comments']) > 0:
			#for comment in new_data['comments']:
				#TODO: Insert comments into comment database

                return jsonify(new_data)
	elif command == 'DELETE SUBREDDIT':
		subreddit = request.form['subreddit']
		db.delete_reddit_posts_from_subreddit(subreddit)
		db.commit()

		scraper = RedditScraper(data_path='./scrapers/data')
		scraper.delete_stored_submissions(subreddit=subreddit)

		return 'Done'
	else:
		print("ERROR: Unknown change request")
		return "ERROR"
	return "Done"


if __name__ == "__main__":
	app.run(host='0.0.0.0')
