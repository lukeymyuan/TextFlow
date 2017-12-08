import sqlite3
import os
from scrapers.reddit_scraper import RedditScraper
from scrapers.twitter_scraper import TwitterScraper

import math

conn = sqlite3.connect("documents.db")
cursor = conn.cursor()



def clearDB(cursor):
    cursor.execute("""DROP TABLE document;""")

def initDB(cursor):
    sql_command = """
    CREATE TABLE IF NOT EXISTS document (
    docID INTEGER PRIMARY KEY,
    source VARCHAR(30),
    content TEXT
    );
    """
    cursor.execute(sql_command)

def initTest(cursor):
    sql_command = """INSERT INTO document (docID, source, content)
    VALUES (NULL, "Twitter", "Testing");"""
    cursor.execute(sql_command)



def init_DB(cursor):
	# Tables
	sql_reddit_submission_command = """
	CREATE TABLE IF NOT EXISTS RedditSubmission (
	id VARCHAR(16) PRIMARY key,
	score INTEGER,
	author VARCHAR(30) NOT NULL,
	golds INTEGER,
	url VARCHAR(100),
	subreddit VARCHAR(20),
	time TIMESTAMP NOT NULL,
	nsfw BOOLEAN,
	title VARCHAR(128),
	text TEXT NOT NULL
	);"""

	sql_reddit_comment_command = """
	CREATE TABLE IF NOT EXISTS RedditComment (
	id VARCHAR(30) PRIMARY key,
	score INTEGER,
	author VARCHAR(30) NOT NULL,
	golds INTEGER,
	subreddit VARCHAR(20),
	time TIMESTAMP NOT NULL,
	submissionID VARCHAR(16),
	text TEXT NOT NULL
	);"""

	sql_tweet_command = """
	CREATE TABLE IF NOT EXISTS Tweet (
	id VARCHAR(20) PRIMARY key,
	author VARCHAR(30) NOT NULL,
	time TIMESTAMP,
	favorites INTEGER,
	retweets INTEGER,
	text TEXT NOT NULL
	);"""

	sql_hashtag_command = """
	CREATE TABLE IF NOT EXISTS ContainsHashtag (
	tweet_id VARCHAR(20) NOT NULL,
	hashtag VARCHAR(64) NOT NULL,
	FOREIGN KEY (tweet_id) REFERENCES Tweet(id),
	PRIMARY KEY (tweet_id, hashtag)
	);"""

	sql_book_command = """
	CREATE TABLE IF NOT EXISTS Book (
	id VARCHAR(10) PRIMARY KEY,
	author VARCHAR(64),
	title VARCHAR(64),
	time TIMESTAMP,
	text TEXT
	);"""

	sql_generic_command = """
	CREATE TABLE IF NOT EXISTS Generic (
	id VARCHAR(32) PRIMARY KEY,
	name VARCHAR(64),
	text TEXT
	);"""

	sql_tags_command = """
	CREATE TABLE IF NOT EXISTS HasTag (
	generic_id VARCHAR(32) NOT NULL,
	tag VARCHAR(32) NOT NULL,
	FOREIGN KEY (generic_id) REFERENCES Generic(id),
        PRIMARY KEY (generic_id, tag)
	);"""

	# Triggers
	sql_tweet_trigger_command = """
	CREATE TRIGGER IF NOT EXISTS DeleteHashtagsTrigger
		BEFORE DELETE ON Tweet
	BEGIN
		DELETE FROM ContainsHashtag WHERE OLD.id = tweet_id;
	END;
	"""

	sql_generic_tag_command = """
	CREATE TRIGGER IF NOT EXISTS DeleteTagsTrigger
		BEFORE DELETE ON Generic
	BEGIN
		DELETE FROM HasTag WHERE OLD.id = generic_id;
	END;
	"""
	# Views
	sql_view_command = """
	CREATE VIEW IF NOT EXISTS Combined AS
	SELECT id, author, text, time FROM RedditSubmission
	UNION ALL
	SELECT id, author, text, time FROM RedditComment
	UNION ALL
	SELECT id, author, text, time FROM Tweet
	UNION ALL
	SELECT id, author, text, time FROM Book
	"""

	print("Creating table RedditSubmission...")
	cursor.execute(sql_reddit_submission_command)
	print("Creating table RedditComment...")
	cursor.execute(sql_reddit_comment_command)
	print("Creating table Tweet...")
	cursor.execute(sql_tweet_command)
	print("Creating table ContainsHashtag...")
	cursor.execute(sql_hashtag_command)
	print("Creating table Book...")
	cursor.execute(sql_book_command)
	print("Creating table Generic...")
	cursor.execute(sql_generic_command)
	print("Creating table HasTag...")
	cursor.execute(sql_tags_command)
	print("Creating Trigger for ContainsHashtag...")
	cursor.execute(sql_tweet_trigger_command)
	print("Creating Trigger for HasTag...")
	cursor.execute(sql_generic_tag_command)
	print("Creating View...")
	cursor.execute(sql_view_command)


def drop_table(cursor, table_name):
	print("Dropping table " + str(table_name) + "...")
	cursor.execute("""DROP TABLE IF EXISTS """ + str(table_name) + """;""")

def drop_trigger(cursor, trigger_name):
	print("Dropping trigger " + str(trigger_name) + "...")
	cursor.execute("""DROP TRIGGER IF EXISTS """ + str(trigger_name) + """;""")

def clear_DB(cursor):
	drop_table(cursor,"RedditSubmission")
	drop_table(cursor,"RedditComment")
	drop_table(cursor,"Tweet")
	drop_table(cursor,"ContainsHashtag")
	drop_table(cursor,"Book")
	drop_table(cursor,"Generic")
	drop_table(cursor,"HasTag")
	drop_trigger(cursor, "DeleteHashtagsTrigger")
	drop_trigger(cursor, "DeleteTagsTrigger")

def insert_generated_text(text):
    query = """
    INSERT INTO GeneratedTexts ( text)
    VALUES (?)
    """

def delete_reddit_posts_from_subreddit(subreddit):
	query = """DELETE FROM RedditSubmission WHERE UPPER(subreddit)=UPPER(?)"""
	print(query)
	args = (subreddit,)
	execute(query, args)

def delete_reddit_post(id):
	query = """DELETE FROM RedditSubmission WHERE id=?"""
	print(query)
	args = (id,)
	execute(query, args)

def update_reddit_post(submission):
	delete_reddit_post(submission['id'])
	insert_reddit_post(submission)
 
def insert_reddit_post(submission):
	query="""
	INSERT OR IGNORE INTO RedditSubmission ( id, score, author, golds, url, subreddit, time, nsfw, title, text) 
	VALUES (?,?,?,?,?,?,?,?,?,?) 
	"""
	print(query)
	args = (
		submission['id'],
		submission['score'],
		submission['author'],
		submission['golds'],
		submission['url'],
		submission['subreddit'],
		int(submission['time']),
		1 if submission['nsfw'] else 0,
		submission['title'],
		submission['text']
	)
	execute(query, args)

def generateID(id):
    return id

def closeDB(save=True):
    global conn
    if save:
        conn.commit()
    conn.close()

def commit():
    conn.commit()

def execute(command, args = None):
    global cursor
    if args:
        cursor.execute(command, args)
    else:
        cursor.execute(command)
    return cursor.fetchall()

def get_table_names():
	tables = execute("""SELECT * FROM sqlite_master WHERE type='table';""")
	names = []
	for item in tables:
		names.append(str(item[1]))
	return names

def get_trigger_names():
	triggers = execute("""SELECT * FROM sqlite_master WHERE type='trigger';""")
	names = []
	for item in triggers:
		names.append(str(item[1]))
	return names

def get_view_names():
	views = execute("""SELECT * FROM sqlite_master WHERE type='view';""")
	names = []
	for item in views:
		names.append(str(item[1]))
	return names

# Table Specific

# Reddit Submissions
def insert_reddit_submission(submission):
    query="""
    INSERT OR IGNORE INTO RedditSubmission ( id, score, author, golds, url, subreddit, time, nsfw, title, text) 
    VALUES (?,?,?,?,?,?,?,?,?,?) 
    """
    #print(query)
    args = (
        submission['id'],
        submission['score'],
        submission['author'],
        submission['golds'],
        submission['url'],
        submission['subreddit'],
        int(submission['time']),
        1 if submission['nsfw'] else 0,
        submission['title'],
        submission['text']
    )
    execute(query, args)

def delete_reddit_submission(id=None, subreddit=None, author=None):
	query = """DELETE FROM RedditSubmission"""
	filters = []
	arg_list = []
	if id != None:
		filters.append('id=?')
		arg_list.append(id)
	if subreddit != None:
		filters.append('UPPER(subreddit)=UPPER(?)')
		arg_list.append(subreddit)
	if author != None:
		filters.append('author=?')
		arg_list.append(author)
	
	query += " WHERE " + " AND ".join(filters)

	#print(query)
	args = tuple(arg_list)
	execute(query, args)

def scrape_reddit_submissions(amount=100, subreddit=None, author=None):
	scraper = RedditScraper(data_path='./scrapers/data/reddit/')
	items = []
	if subreddit != None:
		items = scraper.scrape_submissions(subreddit=subreddit, count=amount)
	elif author != None:
		items, comments = scraper.scrape_user(user=author,submission_count=amount,comment_count=0)

	for item in items:
		insert_reddit_submission(item)
	commit()

def scrape_reddit_comments(amount=100, subreddit=None, author=None):
    scraper = RedditScraper(data_path='./scrapers/data/reddit/')
    items = []
    if subreddit != None:
        items = scraper.scrape_comments(subreddit=subreddit, submission_count=math.ceil(100), comments_per_sub=10)
    elif author != None:
        subs, items = scraper.scrape_user(user=author,submission_count=0,comment_count=amount)

    for item in items:
        insert_reddit_comment(item)
    commit()

# Reddit Comments
def insert_reddit_comment(item):
    query="""
    INSERT OR IGNORE INTO RedditComment ( id, score, author, golds, subreddit, time, submissionID, text) 
    VALUES (?,?,?,?,?,?,?,?) 
    """
    #print(query)
    args = (
        item['id'],
        item['score'],
        item['author'],
        item['golds'],
        item['subreddit'],
        int(item['time']),
        item['submission'],
        item['text']
    )
    execute(query, args)

def delete_reddit_comment(id=None, subreddit=None, author=None):
    query = """DELETE FROM RedditComment"""
    filters = []
    arg_list = []
    if id != None:
        filters.append('id=?')
        arg_list.append(id)
    if subreddit != None:
        filters.append('UPPER(subreddit)=UPPER(?)')
        arg_list.append(subreddit)
    if author != None:
        filters.append('author=?')
        arg_list.append(author)

    query += " WHERE " + " AND ".join(filters)

    #print(query)
    args = tuple(arg_list)
    execute(query, args)

# Tweets

def insert_tweet(item):
	query="""
	INSERT OR IGNORE INTO Tweet ( id, author, time, favorites, retweets, text) 
	VALUES (?,?,?,?,?,?) 
	"""
	args = (
		str(item['id']),
		str(item['author']),
		int(item['time']),
		item['favorite_count'],
		item['retweet_count'],
		item['text']
	)
	
	hashtags = sum(item['hashtags'],[]) # Flatten
	
	execute(query, args)
	for hashtag in hashtags:
		insert_hashtag(str(item['id']), hashtag)

def delete_tweets_with_hashtag(hashtag):
	query = "SELECT tweet_id FROM ContainsHashtag WHERE UPPER(hashtag)=UPPER(\"" + hashtag + "\")"
	tweet_ids = execute(query)
	tweet_ids = [t[0] for t in tweet_ids]
	
	for id in tweet_ids:
		query_t = "DELETE FROM Tweet WHERE id=\"" + str(id) + "\""
		execute(query_t)

def delete_tweet(id=None, author=None):
    query = """DELETE FROM Tweet"""
    filters = []
    arg_list = []
    if id != None:
        filters.append('id=?')
        arg_list.append(id)
    if author != None:
        filters.append('author=?')
        arg_list.append(author)

    query += " WHERE " + " AND ".join(filters)

    #print(query)
    args = tuple(arg_list)
    execute(query, args)


def insert_hashtag(tweet_id, hashtag):
	query="""
	INSERT OR IGNORE INTO ContainsHashtag ( tweet_id, hashtag)
	VALUES (?,?)
	"""
	args = (str(tweet_id), hashtag)
	execute(query, args)

def scrape_twitter_hashtag(hashtag, amount=100):
	scraper = TwitterScraper(data_path='./scrapers/data/twitter')
	items = scraper.scrape_hashtag(hashtag, limit=amount)
        try: 
            for item in items:
		insert_tweet(item)
            commit()
        except sql.Error:
            print("Failed to scrape twitter hashtag. Rolling back");
            conn.rollback()
            raise
def scrape_twitter_user(user, amount=100):
	scraper = TwitterScraper(data_path='./scrapers/data/twitter')
	items = scraper.scrape_user(user, limit=amount)
	for item in items:
		insert_tweet(item)
	commit()



# Book
def insert_book(item):
    query="""
    INSERT OR IGNORE INTO Book ( id, title, author, time, text) 
    VALUES (?,?,?,?,?) 
    """
    args = (
        item['id'],
        item['title'],
        item['author'],
        int(item['time']),
        item['text']
    )
    execute(query, args)



if __name__ == "__main__":
	init_DB(cursor)
	print("Tables: " + ','.join(get_table_names()))
	print("Triggers: " + ','.join(get_trigger_names()))
	print("Views: " + ','.join(get_view_names()))

	scrape_twitter_user("realDonaldTrump",amount=10)

	#all = list(execute("SELECT id FROM Combined"))
	#print("All: " + str(len(all)))	

	#scrape_reddit_comments(amount=110, subreddit='AskRetail')

	#delete_tweets_with_hashtag("UIUC")

	#tweets = list(execute("SELECT tweet_id FROM ContainsHashtag WHERE hashtag=\"UIUC\""))
	#print(tweets)

	#clear_DB(cursor)
	#print("Tables: " + ','.join(get_table_names()))
	#print("Triggers: " + ','.join(get_trigger_names()))
	#print(get_table_names())
	#init_DB(cursor)
	#print(get_table_names())
	#sync_RedditSubmission_with_scraper()

	#tweets = list(execute("""SELECT id FROM Tweet"""))
	#print("Tweets:",len(tweets))

	#books = list(execute("""SELECT id, author, title, time FROM Book"""))
	#print("Books:",len(books))

	#index = 22
	#tweet = tweets[index]
	#tweet_id = str(tweet[0])
	#print("ID: " + str(tweet_id))

	#execute("""DELETE FROM Tweet WHERE id=135091284309319680""")

	#hashtags = execute("""SELECT hashtag FROM ContainsHashtag WHERE tweet_id="""+"135091284309319680")
	#hashtags = [list(t)[0] for t in hashtags]
	#print("Hashtags: " + ', '.join(hashtags))

	#hashtags = list(execute("""SELECT * FROM ContainsHashtag"""))
	#print("Hashtags:",len(hashtags))
	#print(hashtags[0])

