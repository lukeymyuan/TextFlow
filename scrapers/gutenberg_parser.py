import re
import os
import json
import time
import datetime

DEFAULT_DATA_PATH = './data/gutenberg'

class Colors:
	BLUE = '\033[94m'
	SUCCESS = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	DARKGREY='\033[90m'


class GutenbergParser:
	def __init__(self, data_path=None):
		self.set_data_path(data_path)
		self.initialize_data_dirs()

	def set_data_path(self, data_path):
		# Sets the appropriate paths for different data folders
		if data_path == None:
			self.data_path = DEFAULT_DATA_PATH
		else:
			self.data_path = data_path

		self.data_file_path = os.path.join(self.data_path, 'books.json')

	def initialize_data_dirs(self):
		# Create the appropriate data directories if they do not already exist
		dirs_to_create = [self.data_path]
		for dir_path in dirs_to_create:
			if not os.path.exists(dir_path):
				os.makedirs(dir_path)
				self.log("Created directory " + dir_path)

	def parse_file(self, filepath, max_chars=None):
		if os.path.isfile(filepath):
			try:
				with open(filepath, 'r') as f:
					lines = f.readlines()
					id = int(os.path.basename(filepath).split('.')[0])
					return self.parse_lines(lines, id=id, max_chars=max_chars)
			except:
				self.log_error("Couldn't Read File")
		else:
			self.log_error("File " + filepath + " doesn't exist")
		return None

	def parse_lines(self, lines, id, max_chars=None):
		book = None
		try:
			title = None
			author = None
			time = None
			start_recording = False
			final_lines = []
			total_chars = 0
			for i in range(len(lines)):
				line = lines[i]
				if start_recording == False:
					if author == None and line.startswith('Author: '):
						author = re.search('Author: (.*)', line).group(1).strip()
					elif title == None and line.startswith('Title: '):
						title = re.search('Title: (.*)', line).group(1).strip()
						j = i+1
						while lines[j] != '\n':
							title += lines[j].strip()
							j += 1
					# elif time == None and line.startswith('Posting Date: '):
					# 	time = re.search('Posting Date: (.*)\[', line).group(1).strip()
					elif time == None and line.startswith('Release Date: '):
						time = re.search('Release Date: (.*) \[', line).group(1).strip()
					elif line.startswith('*** START OF THIS PROJECT GUTENBERG EBOOK'):
						start_recording = True;

				if start_recording:
					if line.startswith('End of the Project Gutenberg EBook'):
						break

					final_lines.append(line)

					if max_chars != None:
						total_chars += len(line)
						if total_chars >= max_chars:
							break

			if start_recording == True:
				# Read some of the book
				book = dict()
				book['id'] = str(id)
				book['title'] = title
				book['author'] = author
				book['time'] = self.date_to_unix(time)
				book['date'] = time
				book['text'] = ''.join(final_lines)
		except:
			self.log_warning('Ran into error while parsing lines.')

		return book

	def store_books(self, books):
		data = self.load_books()
		prev_count = len(data)
		for book in books:
			data[str(book['id'])] = book
		new_count = len(data.keys())

		with open(self.data_file_path, 'w+') as data_file:    
			json.dump(data, data_file)

		self.log_success("Stored " + str(new_count-prev_count) + " new books [total=" + str(new_count) + "]")

	def load_books(self):
		data = dict()
		if os.path.exists(self.data_file_path):
			try:
				with open(self.data_file_path, 'r') as data_file:
					data = json.load(data_file)
			except:
				self.log_error("Error reading in data for" + self.data_file_path + "(most likely an empty file)")

		return data

	def clear_stored_books(self):
		empty_data = dict()
		with open(self.data_file_path, 'w+') as data_file:    
			json.dump(empty_data, data_file)

	def is_valid_book(self, book):
		if isinstance(book, dict):
			if 'id' in book and 'title' in book and book['title'] != None and book['author'] != None and 'time' in book and book['time'] != None:
				return True
		return False

	def date_to_unix(self, s):
		month = 'january'
		day = '01'
		year = '1905'

		parts = s.strip().split(' ')
		try:
			if len(parts) == 3:
				month = parts[0].lower()
				day = parts[1].replace(',','')
				if len(day) == 1:
					day = '0' + day
				year = parts[2]
			elif len(parts) == 2:
				month = parts[0].replace(',','').lower()
				day = '01'
				year = parts[1]
		except:
			self.log_warning('Unable to format date')


		md = dict()
		md['january'] = '01'
		md['february'] = '02'
		md['march'] = '03'
		md['april'] = '04'
		md['may'] = '05'
		md['june'] = '06'
		md['july'] = '07'
		md['august'] = '08'
		md['september'] = '09'
		md['october'] = '10'
		md['november'] = '11'
		md['december'] = '12'

		month = md[month]

		dateStr = year + '-' + month + '-' + day
		# print(s," | ",dateStr)
		try:
			unix = time.mktime(datetime.datetime.strptime(dateStr, "%Y-%m-%d").timetuple())
		except:
			self.log_warning('Time out of range')
			unix = 0.0

		return unix

		

	def log(self, message):
		print(Colors.DARKGREY + "[GutenbergParser] " + message + Colors.RESET)

	def log_warning(self, warning):
		print(Colors.WARNING + "[GutenbergParser] WARNING: " + warning + Colors.RESET)

	def log_error(self, error):
		print(Colors.FAIL + "[GutenbergParser] ERROR: " + error + Colors.RESET)

	def log_success(self, message):
		print(Colors.SUCCESS + "[GutenbergParser] " + message + Colors.RESET)

	def print_data_summary(self):
		books = self.load_books()
		self.log("Has a total of " + str(len(books)) + " stored.")


def parse_and_store_downloaded_books():
	parser = GutenbergParser()
	books = []
	total = 55000
	# total = 1000
	for i in range(1,total):
		if i % 500 == 0:
			parser.log(" (" + str(i) + " / " + str(total) + ")")
		filename = '/Users/alec/Desktop/gutenberg/' + str(i) + ".txt"
		if os.path.isfile(filename):
			book = parser.parse_file(filename, max_chars=10000)
			if parser.is_valid_book(book):
				books.append(book)
	print(len(books))
	parser.store_books(books)

if __name__ == "__main__":
	parser = GutenbergParser()
	books = parser.load_books()
	for i in range(1000):
		for key in books:
			book = books[key]
			print(book['time']," | ",book['date'])

	# parse_and_store_downloaded_books()

	# parse_and_store_downloaded_books()
	# parser.print_data_summary()
	# books = parser.load_books()
	# print("Books:",len(books))
	# title_and_author = 0
	# books_with_both = []
	# for book in books:
	# 	if book['title'] != None and book['author'] != None and book['time'] != None:
	# 		title_and_author += 1
	# print("Both:",title_and_author)






