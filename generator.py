'''
Reponses will always contain the following keys

(1) result_count : Number of results returned by the query.
(2) server_time : Number of seconds the request took on this server. 

Each reponse type will also contain keys unique to that type.

'''
import time
import random
from datetime import datetime, timedelta
import markov
import db
import random

# TODO: Make sure this works with timezones
def datetime_to_unix_timestamp(dt):
	return time.mktime(dt.timetuple())



'''
Generate a Reddit Submission Response

Unique Keys:
(1) title : The generated title of the post
(2) selftext : The generated selftext of the post (may be empty)
(3) url : The selected url for the post (may be empty)
(4) examples : A small sample of the full results
'''
def generate_reddit_submission(req):
	# Get the relevant data from the request
	source = req['source']
	subreddit = req['subreddit']
	author = req['author']
	time_period = req['time_period']
	degree = 1
	if 'degree' in req:
		degree = req['degree']

	# Format the data from the request
	if source != 'RedditSubmission':
		print('ERROR: Tried to generate Reddit submission from the source "{0}"'.format(source))
		return None

	oldest_time = None
	if time_period.lower() != 'all':
		# Need to filter results by time
		days_to_subtract = 0;
		if time_period.lower() == 'today':
			days_to_subtract = 1
		elif time_period.lower() == 'past week':
			days_to_subtract = 7
		elif time_period.lower() == 'past month':
                        days_to_subtract = 30
		elif time_period.lower() == 'past year':
                        days_to_subtract = 365
		oldest_time = datetime.now() - timedelta(days=days_to_subtract)
		oldest_time = datetime_to_unix_timestamp(oldest_time)

	# Create the filters
	filters = []
	if subreddit != '':
		filters.append('UPPER(subreddit)=UPPER("{0}")'.format(subreddit))
	if author != '':
		filters.append('author="{0}"'.format(author))
	if oldest_time != None:
		filters.append('time>="{0}"'.format(str(oldest_time)))

	# Form the query
	query = """SELECT title, text, url, author, score, subreddit FROM {0}""".format(source)

	if len(filters) > 0:
		query+="\nWHERE "+" AND ".join(filters)

	print(query)

	# Execute the query
	result = db.execute(query)

	# Check if any results matches the request
	if len(result) > 0:
		titles, texts, urls, authors, scores, subreddits = zip(*result)


		# Generate the Reddit submission
		total_title_len = 0
		for title in titles:
			total_title_len += len(title.split(' '))
		avg_title_len = total_title_len / len(titles)
	
		title = markov.generate(' '.join(titles), avg_title_len, degree)
		selftext, d = markov.generate(' '.join(texts), max(50,len(random.choice(texts).split())), degree, True)
                print(selftext)
		url = random.choice(urls)
		examples = []
		max_example_count = 20
		for i in range(len(titles)):
			if i >= max_example_count:
				break
			else:
				examples.append({
					'title':titles[i],
					'selftext':texts[i],
					'url':urls[i],
					'author':authors[i],
					'score':scores[i],
					'subreddit':subreddits[i]
				})
	else:
		title = ''
		selftext = ''
		url = ''
		examples = []


	# Get total number of results
	result_count = len(result)
	
	# Compose the response
	response = {
		'result_count': result_count,
		'title': title,
		'selftext': selftext,
		'url': url,
		'examples': examples
	}
	return response

def generate_reddit_comment(req):
    # Get the relevant data from the request
    source = req['source']
    subreddit = req['subreddit']
    author = req['author']
    time_period = req['time_period']

    degree = 1 
    if 'degree' in req:
        degree = req['degree']

    oldest_time = None
    if time_period.lower() != 'all':
        # Need to filter results by time
        days_to_subtract = 0;
        if time_period.lower() == 'today':
            days_to_subtract = 1
        elif time_period.lower() == 'past week':
            days_to_subtract = 7
        elif time_period.lower() == 'past month':
                        days_to_subtract = 30
        elif time_period.lower() == 'past year':
                        days_to_subtract = 365
        oldest_time = datetime.now() - timedelta(days=days_to_subtract)
        oldest_time = datetime_to_unix_timestamp(oldest_time)

	
    # Create the filters
    filters = []
    if subreddit != '':
        filters.append('UPPER(subreddit)=UPPER("{0}")'.format(subreddit))
    if author != '':
        filters.append('author="{0}"'.format(author))
    if oldest_time != None:
        filters.append('time>="{0}"'.format(str(oldest_time)))

    # Form the query
    query = """SELECT text, author, score, subreddit, time FROM {0}""".format(source)

    if len(filters) > 0:
        query+="\nWHERE "+" AND ".join(filters)

    print(query)

    # Execute the query
    result = db.execute(query)	


    # Check if any results matches the request
    if len(result) > 0:
        texts, authors, scores, subreddits, times = zip(*result)

        # Generate the Reddit comment
        count = len(random.choice(texts).split())
        gentext = markov.generate(' '.join(texts), count, degree)
        examples = []
        max_example_count = 20
        for i in range(len(texts)):
            if i >= max_example_count:
                break
            else:
                examples.append({
                    'text':texts[i],
                    'author':authors[i],
                    'score':scores[i],
                    'subreddit':subreddits[i],
					'time':times[i]
                })
    else:
        gentext = ''
        examples = []

    # Get total number of results
    result_count = len(result)

    # Compose the response
    response = {
        'result_count': result_count,
        'text': gentext,
        'examples': examples
    }

    return response

def generate_tweet(req):
    # Get the relevant data from the request
    source = req['source']
    hashtag = req['hashtag']
    author = req['author']
    time_period = req['time_period']

    degree = 1 
    if 'degree' in req:
        degree = req['degree']

    oldest_time = None
    if time_period.lower() != 'all':
        # Need to filter results by time
        days_to_subtract = 0;
        if time_period.lower() == 'today':
            days_to_subtract = 1
        elif time_period.lower() == 'past week':
            days_to_subtract = 7
        elif time_period.lower() == 'past month':
                        days_to_subtract = 30
        elif time_period.lower() == 'past year':
                        days_to_subtract = 365
        oldest_time = datetime.now() - timedelta(days=days_to_subtract)
        oldest_time = datetime_to_unix_timestamp(oldest_time)


    # Create the filters
    filters = []
    #if hashtag != '':
    #    filters.append('UPPER(hashtag)=UPPER("{0}")'.format(hashtag))
    if author != '':
        filters.append('author="{0}"'.format(author))
    if oldest_time != None:
        filters.append('time>="{0}"'.format(str(oldest_time)))

    # Form the query
    query = ""
    if hashtag != '':
        query = """
        SELECT text, author, favorites, retweets, time
        FROM Tweet as T, ContainsHashtag as H
        WHERE T.id == H.tweet_id AND UPPER(H.hashtag) = UPPER("{0}") """.format(str(hashtag))
        if len(filters) > 0:
            query += "AND " + " AND ".join(filters)
    else:
        query = """
        SELECT text, author, favorites, retweets, time
        FROM Tweet
        """
        if len(filters) > 0:
            query += " WHERE " + " AND ".join(filters)


    print(query)

    # Execute the query
    result = db.execute(query)


    # Check if any results matches the request
    if len(result) > 0:
        texts, authors, favorites, retweets, times = zip(*result)

        # Generate the Tweet
        count = len(random.choice(texts).split())
        gentext = markov.generate(' '.join(texts), count, degree)
        examples = []
        max_example_count = 20
        for i in range(len(texts)):
            if i >= max_example_count:
                break
            else:
                examples.append({
                    'text':texts[i],
                    'author':authors[i],
                    'favorites':favorites[i],
                    'retweets':retweets[i],
                    'time':times[i]
                })
    else:
        gentext = ''
        examples = []

    # Get total number of results
    result_count = len(result)
	
    # Compose the response
    response = {
        'result_count': result_count,
        'text': gentext,
        'examples': examples
    }

    return response


def generate_book(req):
    # Get the relevant data from the request
    source = req['source']
    title = req['title']
    author = req['author']
    time_period = req['time_period']

    degree = 1 
    if 'degree' in req:
        degree = req['degree']

    oldest_time = None
    if time_period.lower() != 'all':
        # Need to filter results by time
        days_to_subtract = 0;
        if time_period.lower() == 'past year':
            days_to_subtract = 365
        elif time_period.lower() == 'past decade':
            days_to_subtract = 365*10
        elif time_period.lower() == 'past century':
            days_to_subtract = 365*100
        oldest_time = datetime.now() - timedelta(days=days_to_subtract)
        oldest_time = datetime_to_unix_timestamp(oldest_time)


    # Create the filters
    filters = []
    if author != '':
        filters.append('UPPER(author)=UPPER("{0}")'.format(author))
    if title != '':
        filters.append('UPPER(title)=UPPER("{0}")'.format(title))
    if oldest_time != None:
        filters.append('time>="{0}"'.format(str(oldest_time)))

    LIMIT = 1000
    # Form the query
    query = """SELECT title, author, text, time FROM Book"""
    if len(filters) > 0:
        query+="\n WHERE "+" AND ".join(filters)    
    else:
        query = """SELECT title, author, text, time FROM Book WHERE id IN (SELECT id FROM Book ORDER BY RANDOM() LIMIT 1000)"""


    print(query)

    # Execute the query
    result = db.execute(query)
    #print("Query finished")
    #print(result)

    # Check if any results matches the request
    if len(result) > 0:
        titles, authors, texts, times = zip(*result)

        max_samples = 100
        if len(texts) > max_samples:
            texts = random.sample(texts,max_samples)

        # Generate the book
        count = len(random.choice(texts).split())
        gentext = markov.generate(' '.join(texts), count, degree)
        examples = []
        max_example_count = 5
        for i in range(len(texts)):
            if i >= max_example_count:
                break
            else:
                examples.append({
                    'text':texts[i],
                    'author':authors[i],
                    'title':titles[i],
                    'time':times[i]
                })
    else:
        gentext = ''
        examples = []

    # Get total number of results
    result_count = len(result)

    # Compose the response
    response = {
        'result_count': result_count,
        'text': gentext,
        'examples': examples
    }

    return response


def generate_custom(req):
	text = req['text']
	length = 100
	if 'length' in req:
		length = req['length']

	degree = 1 
	if 'degree' in req:
		degree = req['degree']

	gen_text = markov.generate(text, length, degree)

	response = {
		'text': gen_text
	}
	return response


def generate_generic(req):
	print("TODO")
	return dict()

def generate_combined(req):
    # Get the relevant data from the request
    author = req['author']
    time_period = req['time_period']

    degree = 1 
    if 'degree' in req:
        degree = req['degree']

    oldest_time = None
    if time_period.lower() != 'all':
        # Need to filter results by time
        days_to_subtract = 0;
        if time_period.lower() == 'past year':
            days_to_subtract = 365
	elif time_period.lower() == 'past month':
            days_to_subtract = 30
        elif time_period.lower() == 'past decade':
            days_to_subtract = 365*10
        elif time_period.lower() == 'past century':
            days_to_subtract = 365*100
        oldest_time = datetime.now() - timedelta(days=days_to_subtract)
        oldest_time = datetime_to_unix_timestamp(oldest_time)

    # Create the filters
    filters = []
    if author != '':
        filters.append('UPPER(author)=UPPER("{0}")'.format(author))
    if oldest_time != None:
        filters.append('time>="{0}"'.format(str(oldest_time)))

    # Form the query
    query = """SELECT author, text, time FROM Combined"""
    
    if len(filters) > 0:
        query+="\nWHERE "+" AND ".join(filters)
    else:
        query = """SELECT author, text, time FROM Combined WHERE id IN (SELECT id FROM Combined ORDER BY RANDOM() LIMIT 1000)"""
    print(query)

    # Execute the query
    result = db.execute(query)

    # Check if any results matches the request
    if len(result) > 0:
        authors, texts, times = zip(*result)

        max_samples = 5000
        if len(texts) > max_samples:
            texts = random.sample(texts,max_samples)

        # Generate the book
        count = max(50,len(random.choice(texts).split()))

        gentext = markov.generate(' '.join(texts), count, degree)
        examples = []
        max_example_count = 10
        for i in range(len(texts)):
            if i >= max_example_count:
                break
            else:
                examples.append({
                    'text':texts[i],
                    'author':authors[i],
                    'time':times[i]
                })
    else:
        gentext = ''
        examples = []

    # Get total number of results
    result_count = len(result)

    # Compose the response
    response = {
        'result_count': result_count,
        'text': gentext,
        'examples': examples
    }

    return response













if __name__ == "__main__":
	#request = {'subreddit':'','time_period':'all','author':'', 'source':'RedditComment'}
	#print("Request: " + str(request))
	#response = generate_reddit_comment(request)
	#print(response)	

	#request = {'hashtag':'UIUC','time_period':'all','author':'SunnyChopper', 'source':'Tweet'}
	#print("Request: " + str(request))
	#response = generate_tweet(request)
	#print(response)

    request = {'title':'', 'author':'Bram Stoker','time_period':'all', 'source':'Book'}
    #print("Request: " + str(request))
    response = generate_book(request)
    print(response['text'])
    #request = {'author':'','time_period':'all'}
    #print("Request: " + str(request))
    #response = generate_combined(request)
    #print(response['text'])
    #for example in response['examples']:
	#print(example['author'])
    #print(response['result_count'])


