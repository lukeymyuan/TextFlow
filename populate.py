import db
import json
import os
from scrapers.reddit_scraper import RedditScraper
from scrapers.twitter_scraper import TwitterScraper
from scrapers.gutenberg_parser import GutenbergParser

def sync_reddit_submissions():
    query = """SELECT id, score, author, golds, url, subreddit, time, nsfw, title, text FROM RedditSubmission""";
    items = db.execute(query)
    submissions = dict()
    for item in items:
        submission = dict()
        submission['id'] = item[0] 
        submission['score'] = item[1]
        submission['author'] = item[2]
        submission['golds'] = item[3]
        submission['url'] = item[4]
        submission['subreddit'] = item[5]
        submission['time'] = item[6]
        submission['nsfw'] = (item[7] == 1)
        submission['title'] = item[8]
        submission['text'] = item[9]

        sr = submission['subreddit']
        if sr not in submissions:
            submissions[sr] = []

        submissions[sr].append(submission)

	# Store submission in scraper data
    data_path = './scrapers/data/reddit'
    if os.path.isdir(data_path):
        scraper = RedditScraper(data_path=data_path)
        for subreddit in submissions:
            scraper.store_submissions(submissions[subreddit],subreddit)
        all_submissions = scraper.get_all_stored_submissions()
        for subreddit in all_submissions:
            submissions = all_submissions[subreddit]
            for key, submission in submissions.items():
                db.insert_reddit_submission(submission)
        db.commit()
    else:
        print("No directory at " + data_path)


def sync_reddit_comments():
    query = """SELECT id, score, author, golds, subreddit, time, submissionID, text FROM RedditComment""";
    items = db.execute(query)
    data = dict()
    for item in items:
        d = dict()
        d['id'] = item[0]
        d['score'] = item[1]
        d['author'] = item[2]
        d['golds'] = item[3]
        d['subreddit'] = item[4]
        d['time'] = item[5]
        d['submission'] = item[6]
        d['text'] = item[7]

        sr = d['subreddit']
        if sr not in data:
            data[sr] = []

        data[sr].append(d)

    # Store submission in scraper data
    data_path = './scrapers/data/reddit'
    if os.path.isdir(data_path):
        scraper = RedditScraper(data_path=data_path)
        for subreddit in data:
            for comment in data[subreddit]:
                submission_id = comment['submission']
                scraper.store_comments([comment],subreddit,submission_id)
        all_data = scraper.get_all_stored_comments()
        for subreddit in all_data:
            s_data = all_data[subreddit]
            for key, d in s_data.items():
                db.insert_reddit_comment(d)
        db.commit()
    else:
        print("No directory at " + data_path)

def sync_tweets():
    query = """SELECT id, author, time, favorites, retweets, text FROM Tweet"""	
    items = db.execute(query)
    data = []
    for item in items:
        d = dict()
        d['id'] = item[0]
        d['author'] = item[1]
        d['time'] = item[2]
        d['favorite_count'] = item[3]
        d['retweet_count'] = item[4]
        d['text'] = item[5]

        # Get hashtags
        h_query = """SELECT hashtag FROM ContainsHashtag WHERE tweet_id=""" + str(d['id'])
        hashtags = list(db.execute(h_query))
        d['hashtags'] = hashtags

        data.append(d)

    data_path = './scrapers/data/twitter'
    if os.path.isdir(data_path):
        scraper = TwitterScraper(data_path=data_path)
        scraper.store_statuses(data)
        
        all_data = scraper.load_statuses()
        for id, tweet in all_data.items():
            db.insert_tweet(tweet)
        db.commit()
    else:
        print("No directory at " + data_path)

def sync_books():
    query = """SELECT id, title, author, time, text FROM Book"""
    items = db.execute(query)
    data = dict()
    for item in items:
        d = dict()
        d['id'] = item[0]
        d['title'] = item[1]
        d['author'] = item[2]
        d['time'] = item[3]
        d['text'] = item[4]

        data.append(d)

    data_path = './scrapers/data/gutenberg'
    if os.path.isdir(data_path):
        scraper = GutenbergParser(data_path=data_path)
        scraper.store_books(data)

        all_data = scraper.load_books()
        for id, book in all_data.items():
            db.insert_book(book)
        db.commit()
    else:
        print("No directory at " + data_path)

if __name__ == '__main__':
	sync_reddit_submissions()
	sync_reddit_comments()
	#sync_books()
	sync_tweets()

