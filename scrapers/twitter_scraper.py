import tweepy
import os
import json
import time
import pytz

# TODO: Hide the following information
consumer_key = 'bAKSG1H3B5P41VomqFnZwDypd'
consumer_secret = 'ai555hZnowaPm3HK9bq8DSKtMdnGY7shQXh2KIZ7UL5Giyl0yk'
access_token = '926960759891951618-wiSWLGA8QCEzfGZX4ptD3mSluzLKhsw'
access_token_secret = '9AcGdLwz4oadxFwhttVw1E4HpkTmMO77dsI7zuVYnCm3l'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


gmt = pytz.timezone('GMT')
ctz = pytz.timezone('US/Central')

DEFAULT_DATA_PATH = './data/twitter'

example_hashtags = ['Chicago','UIUC','Trump','Christmas','MeToo','traffic','SkirballFire','Los Angeles','Rant','FinalsWeek','College','Funny','coffeebreak','programming','humor','marvel']
example_hashtags_2 = ['BreakingNews','Trump','NotAllMen']


example_users = ['realDonaldTrump','YouTube','POTUS','FoxNews','NFL','CNN','GameOfThrones','BarackObama','taylorswift13','Twitter','cnnbrk','nytimes','espn','Adele','NASA','HillaryClinton','Google','cgpgrey','SpaceX','BradyHaran']

class Colors:
	HEADER = '\033[95m'
	BLUE = '\033[94m'
	SUCCESS = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	LIGHTGREY= '\033[37m'
	DARKGREY='\033[90m'
	YELLOW = '\033[93m'
	LIGHTCYAN='\033[96m'
	GREEN='\033[32m'

class TwitterScraper:
	def __init__(self, data_path=None):
		self.set_data_path(data_path)
		self.initialize_data_dirs()

	def set_data_path(self, data_path):
		# Sets the appropriate paths for different data folders
		if data_path == None:
			self.data_path = DEFAULT_DATA_PATH
		else:
			self.data_path = data_path

		self.tweet_data_path = os.path.join(self.data_path, "tweets")

	def initialize_data_dirs(self):
		# Create the appropriate data directories if they do not already exist
		dirs_to_create = [self.data_path, self.tweet_data_path]

		for dir_path in dirs_to_create:
			if not os.path.exists(dir_path):
				os.makedirs(dir_path)
				self.log("Created directory " + dir_path)

	def scrape_hashtag(self, hashtag, limit=None):
		cursor = tweepy.Cursor(api.search, q=hashtag, count=limit, lang='en', tweet_mode='extended')
		statuses = []
		for status in cursor.items(limit=limit):
			statuses.append(status)
		return self.store_statuses(statuses)


	def scrape_user(self, screen_name, limit=10):
		timeline = api.user_timeline(screen_name = screen_name, count = limit, include_rts = True, tweet_mode='extended')
		statuses = []
		for status in timeline:
			statuses.append(status)
		return self.store_statuses(statuses)

	def store_statuses(self, statuses):
		file_path = os.path.join(self.tweet_data_path, 'statuses.json')

		data = self.load_statuses()

		prev_count = len(data.items())

		new_statuses = []

		for status in statuses:
			f_status = status
			if isinstance(f_status, dict) == False:
				f_status = self.format_status(status)
			if f_status['id'] not in data:
				data[f_status['id']] = f_status
				new_statuses.append(f_status)

		new_count = len(data.items())

		with open(file_path, 'w+') as data_file:    
			json.dump(data, data_file)

		self.log_success("Stored " + str(new_count-prev_count) + " new tweets [total=" + str(new_count) + "]")
		return new_statuses

	def get_hashtags(self, status):
		items = status.entities.get('hashtags')
		hashtags = []
		for item in items:
			hashtags.append(item['text'])
		return sorted(hashtags);

	def get_time(self, status):
		gmt_date = gmt.localize(status.created_at)
		central_date = gmt_date.astimezone(ctz)
		unix = time.mktime(central_date.timetuple())
		return unix

	def format_status(self, status):
		res = {
			'id': str(status.id),
			'author': status.author.screen_name,
			'time': self.get_time(status),
			'favorite_count': status.favorite_count,
			'retweet_count': status.retweet_count,
			'text': status.full_text,
			'hashtags': self.get_hashtags(status)
		}
		return res

	def load_statuses(self):
		file_path = os.path.join(self.tweet_data_path, 'statuses.json')
		data = dict()
		if os.path.exists(file_path):
			try:
				with open(file_path, 'r') as data_file:
					data = json.load(data_file)
			except:
				self.log_error("Error reading in data for", file_path, "(most likely an empty file)")
		return data

	def log(self, message):
		print(Colors.DARKGREY + "[TwitterScraper] " + message + Colors.RESET)

	def log_warning(self, warning):
		print(Colors.WARNING + "[TwitterScraper] WARNING: " + warning + Colors.RESET)

	def log_error(self, error):
		print(Colors.FAIL + "[TwitterScraper] ERROR: " + error + Colors.RESET)

	def log_success(self, message):
		print(Colors.SUCCESS + "[TwitterScraper] " + message + Colors.RESET)

	def print_data_summary(self):
		statuses = self.load_statuses()
		self.log("Total Tweets: " + str(len(statuses.keys())))


if __name__ == "__main__":
	scraper = TwitterScraper()

	## Scrape Users
	# count = 200;
	# i = 0
	# for user in example_users:
	# 	i += 1
	# 	scraper.log('('+ str(i)+ '/' + str(len(example_users)) +')Scraping ' + user + "...")
	# 	scraper.scrape_user(user, limit=count)

	## Scrape Hashtags
	# count = 300;
	# i = 0
	# for hashtag in example_hashtags_2:
	# 	i += 1
	# 	scraper.log('('+ str(i)+ '/' + str(len(example_hashtags)) +')Scraping ' + hashtag + "...")
	# 	scraper.scrape_hashtag(hashtag, limit=count)

	res = scraper.scrape_hashtag('news', limit=10)

	scraper.print_data_summary()






