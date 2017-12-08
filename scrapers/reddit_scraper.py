import praw
import os
import json
import time

username = "scraper_bot"
password = "textflow"
secret = "i8c1fWSpndvNIKex62GwLwswrSs"
public = "KhY-qHlUqbYdPw"
user_agent = "MacOSX: Reddit post scraper:v1.0 (by /u/" + username + ")"

reddit = praw.Reddit(client_id=public, client_secret=secret, user_agent=user_agent)

DEFAULT_DATA_PATH = './data/reddit'

subreddits_to_scrape = sorted(['askreddit','news','movies','pics','funny','iama','todayilearned','videos','worldnews','gifs','gaming','aww','mildlyinteresting','television','music','showerthoughts','tifu','jokes','art','askscience','books','creepy','dataisbeautiful','explainlikeimfive','getmotivated','history','internetisbeautiful','lifeprotips','nottheonion','philosophy','science','space','sports','politics','interestingasfuck','wholesomememes','relationships','subredditsimulator','talesfromtechsupport','talesfromretail','technology','britishproblems','legaladvice','whowouldwin','writingprompts','nosleep','askhistorians','pettyrevenge','prorevenge','osha'])

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

class RedditScraper():

	def __init__(self, data_path=None):
		self.set_data_path(data_path)
		self.initialize_data_dirs()

	def set_data_path(self, data_path):
		# Sets the appropriate paths for different data folders
		if data_path == None:
			self.data_path = DEFAULT_DATA_PATH
		else:
			self.data_path = data_path

		self.submission_data_path = os.path.join(self.data_path, "submissions")
		self.comment_data_path = os.path.join(self.data_path, "comments")

	def initialize_data_dirs(self):
		# Create the appropriate data directories if they do not already exist
		dirs_to_create = [self.data_path, self.submission_data_path, self.comment_data_path]

		for dir_path in dirs_to_create:
			if not os.path.exists(dir_path):
				self.log("Creating directory '{0}'".format(dir_path))
				os.makedirs(dir_path)

	def log(self, message):
		print(Colors.DARKGREY + "[RedditScraper] " + message + Colors.RESET)

	def log_warning(self, warning):
		print(Colors.WARNING + "[RedditScraper] WARNING: " + warning + Colors.RESET)

	def log_error(self, error):
		print(Colors.FAIL + "[RedditScraper] ERROR: " + error + Colors.RESET)

	def log_success(self, message):
		print(Colors.SUCCESS + "[RedditScraper] " + message + Colors.RESET)


	def scrape_subreddits(self, subreddits=['askreddit'], submissions=50, comment_submissions=5, comments_per_sub=50, time_period='all'):
		self.log("Scraping from {0} subreddits...".format(len(subreddits)))
		count = 0
		for subreddit in subreddits:
			self.scrape_subreddit(subreddit, submissions, comment_submissions, comments_per_sub, time_period)
			count += 1
			self.log("{0}/{1} subreddits scraped".format(count,len(subreddits)))

	def scrape_subreddit(self, subreddit='askreddit', submissions=50, comment_submissions=5, comments_per_sub=50, time_period='all'):
		new_submissions = self.scrape_submissions(subreddit, submissions, time_period)
		new_comments = self.scrape_comments(subreddit, comment_submissions, comments_per_sub, time_period)
		return {'submissions':new_submissions,'comments':new_comments}

	def scrape_submissions(self, subreddit='askreddit', count=10, time_period='all'):
		self.log("Scraping {0} submission from the subreddit /r/{1} from top of {2}.".format(count, subreddit, time_period))

		submissions = list(reddit.subreddit(subreddit).top(time_period, limit=count))
		new_submissions = self.store_submissions(submissions, subreddit)
		return new_submissions

	def scrape_comments(self, subreddit='askreddit', submission_count=1, comments_per_sub=10, time_period='all'):
		self.log("Scraping {0} comments from the subreddit /r/{1} from top of {2}.".format(submission_count * comments_per_sub, subreddit, time_period))

		new_comments = []

		submissions = list(reddit.subreddit(subreddit).top(time_period, limit=submission_count))
		for submission in submissions:
			count = 0
			comments = []
			for top_level_comment in submission.comments:
				if type(top_level_comment) != praw.models.reddit.comment.Comment:
					break;
				comments.append(top_level_comment)
				count += 1
				if count >= comments_per_sub:
					break
			new_comments += self.store_comments(comments, subreddit, submission.id)
		return new_comments

	def scrape_user(self, user, submission_count=20, comment_count=100, time_period='all'):
		self.log("Scraping {0} comments and {0} submissions from the user /u/{1} from top of {2}.".format(submission_count, comment_count, user, time_period))
		
		# Submissions
		new_submissions = []
		if submission_count > 0:
			submissions = list(reddit.redditor(user).submissions.top(time_period, limit=submission_count))
			subDict = dict()
			for submission in submissions:
				subreddit = submission.subreddit.display_name
				if subreddit not in subDict:
					subDict[subreddit] = []
				subDict[subreddit].append(submission)
			for subreddit in subDict:
				new_submissions += self.store_submissions(subDict[subreddit],subreddit)



		# Comments
		new_comments = []
		if comment_count > 0:
			comments = list(reddit.redditor(user).comments.top(time_period, limit=comment_count))
			comDict = dict()
			for comment in comments:
				subreddit = comment.subreddit.display_name
				if subreddit not in comDict:
					comDict[subreddit] = []
				comDict[subreddit].append(comment)
			for subreddit in comDict:
				for comment in comDict[subreddit]:
					submission_id = comment.submission.id
					new_comments += self.store_comments([comment],subreddit,submission_id)

		return (new_submissions, new_comments)



	def store_submissions(self, submissions, subreddit):
		file_path = os.path.join(self.submission_data_path, subreddit.lower() + '.json')

		data = {}
		if os.path.exists(file_path):
			try:
				with open(file_path, 'r') as data_file:    
					data = json.load(data_file)
			except:
				self.log_error("Error reading in data for " + file_path + " (most likely an empty file)")

		prev_count = len(data)
		new_submissions = []

		with open(file_path, 'w+') as data_file:    
			for submission in submissions:
				formated = self.format_submission(submission)
				if formated != None:
					id = formated['id']
					if id not in data:
						new_submissions.append(formated)
						data[id] = formated

			new_count = len(data)
			json.dump(data, data_file)

		self.log_success("Stored " + str(new_count-prev_count) + " new submissions for /r/"+subreddit + " [total=" + str(new_count) + "]")
		return new_submissions

	def store_comments(self, comments, subreddit, submission_id):
		file_path = os.path.join(self.comment_data_path, subreddit.lower() + '.json')

		data = {}
		if os.path.exists(file_path):
			try:
				with open(file_path, 'r') as data_file:    
					data = json.load(data_file)
			except:
				self.log_error("Error reading in data for " + file_path + " (most likely an empty file)")

		prev_count = len(data)
		new_comments = []

		with open(file_path, 'w+') as data_file:
			for comment in comments:
				formated = self.format_comment(comment, subreddit, submission_id)
				if formated != None:
					id = formated['id']
					if id not in data:
						new_comments.append(formated)
						data[id] = formated

			new_count = len(data)
			json.dump(data, data_file)

		self.log_success("Stored " + str(new_count-prev_count) + " new comments for /r/"+subreddit + " [total=" + str(new_count) + "]")
		return new_comments


	def format_submission(self, submission):
		author = submission.author
		if author != None:
			author_name = author.name
		else:
			author_name = None

		res = {
			'id': submission.id,
			'score': submission.score,
			'author': author_name,
			'link': submission.shortlink,
			'golds': submission.gilded,
			'url': submission.url,
			'subreddit': submission.subreddit.display_name,
			'time': submission.created_utc,
			'nsfw': submission.over_18,
			'title': submission.title,
			'text': submission.selftext
		}
		return res

	def format_comment(self, comment, subreddit_name, submission_id):

		if type(comment) != praw.models.reddit.comment.Comment:
			# Not a valid comment
			# Probably a MoreComments object
			return None

		author = comment.author
		if author != None:
			author_name = author.name
		else:
			author_name = None

		res = {
			'id':comment.id,
			'score': comment.score,
			'author': author_name,
			'link': comment.permalink,
			'golds': comment.gilded,
			'is_root': comment.is_root,
			# 'depth': comment.depth,
			'edited': comment.edited,
			'submission': submission_id,
			'subreddit': subreddit_name, #comment.subreddit.display_name,
			'time': comment.created_utc,
			'text': comment.body
		}
		return res

	def get_all_stored_submissions(self):
		files = os.listdir(self.submission_data_path)
		subreddits = []
		for filename in files:
			if filename.split('.')[-1] == 'json':
				subreddits.append(filename[0:-5])
		all_submissions = {}
		for subreddit in subreddits:
			all_submissions[subreddit] = self.get_stored_submissions(subreddit)
		return all_submissions

	def get_all_stored_comments(self):
		files = os.listdir(self.comment_data_path)
		subreddits = []
		for filename in files:
			if filename.split('.')[-1] == 'json':
				subreddits.append(filename[0:-5])
		all_comments = {}
		for subreddit in subreddits:
			all_comments[subreddit] = self.get_stored_comments(subreddit)
		return all_comments

	def get_stored_submissions(self, subreddit):
		file_path = os.path.join(self.submission_data_path, subreddit + ".json")
		try:
			with open(file_path, 'r') as data_file:    
				data = json.load(data_file)
				return data
		except:
			self.log_warning("Empty file for /r/" + subreddit)
			return {}

	def get_stored_comments(self, subreddit):
		file_path = os.path.join(self.comment_data_path, subreddit + ".json")
		try:
			with open(file_path, 'r') as data_file:    
				data = json.load(data_file)
				return data
		except:
			self.log_warning("Empty file for /r/" + subreddit)
			return {} 

	def scrape_submission_from_url(self, url):
		return praw.models.Submission(reddit, id=None, url=url, _data=None)

	def scrape_submission_from_id(self, id):
		return praw.models.Submission(reddit, id=id, url=None, _data=None)

	def scrape_comment_from_url(self, url):
		return praw.models.Submission(reddit, id=None, url=url, _data=None).comments[0]

	def scrape_comment_from_id(self, id):
		return praw.models.Comment(reddit, id=id)

	def delete_stored_submissions(self, subreddit):
		path = os.path.join(self.submission_data_path,subreddit+'.json')
		if os.path.exists(path):
			os.remove(path)

	def print_data_summary(self):

		print(Colors.HEADER + "==================================================" + Colors.RESET)
		print(Colors.HEADER + "=               Reddit Data Summary              =" + Colors.RESET)
		print(Colors.HEADER + "==================================================" + Colors.RESET)

		pad = 50

		# Comments

		print("\n==================== COMMENTS ====================\n")
		total_comments = 0
		all_comments = self.get_all_stored_comments()

		count = 0
		for subreddit in list(all_comments.keys()):
			count += 1
			s = "(" + str(count) + ") " + Colors.YELLOW + subreddit + Colors.RESET + " " + Colors.DARKGREY
			p = pad - len(s)
			s += "-"*p + Colors.RESET + " " + Colors.LIGHTCYAN + str(len(all_comments[subreddit])) + Colors.RESET
			total_comments += len(all_comments[subreddit])
			print(s)

		print("TOTAL " + "-"*(pad-20) + " " + str(total_comments))


		# Submissions

		print("\n==================== SUBMISSIONS ====================\n")
		total_submissions = 0
		all_submissions = self.get_all_stored_submissions()

		count = 0
		for subreddit in list(all_submissions.keys()):
			count += 1
			s = "(" + str(count) + ") " + Colors.YELLOW + subreddit + Colors.RESET + " " + Colors.DARKGREY
			p = pad - len(s)
			s += "-"*p + Colors.RESET + " " + Colors.LIGHTCYAN + str(len(all_submissions[subreddit])) + Colors.RESET
			total_submissions += len(all_submissions[subreddit])
			print(s)

		print("TOTAL " + "-"*(pad-20) + " " + str(total_submissions))

		print(Colors.GREEN + "\nCOMMENTS + SUBMISSIONS " + "-"*(pad-30) + " " + str(total_submissions+total_comments) + Colors.RESET)


if __name__ == "__main__":
	scraper = RedditScraper()
	
	scraper.scrape_user(user='spez', submission_count=100, comment_count=200)

	# scraper.print_data_summary()
	# res = scraper.scrape_comments(subreddit='worldnews', submission_count=1, comments_per_sub=2, time_period='day')
	# print(res)

	# scraper.delete_stored_submissions(subreddit='soccer')
	# res = scraper.scrape_submissions(subreddit='soccer', count=1, time_period='day')
	# print(res)

	# scraper.scrape_subreddits(subreddits_to_scrape, 100, 5, 20, 'month')














