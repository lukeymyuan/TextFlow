# TextFlow
### Summary
A general purpose web application for generating text from various sources (books, academic papers, tweets, facebook posts, and reddit posts). The text will match the semantic style of the author(s) selected by the user using markov chain text generation techniques.

### Demo
<https://www.youtube.com/watch?v=tTQXbw1gR-o>

### Important files:

#### app.py
This is the file that runs the server

#### markov_final.py
This is the file that contains the python code for the Markov text generation algorithm.  The function takes the following three arguments:
	source:  The input text source that the generated text will be generated from
	length:  The number of words to generate
	lookback:  The number of words used as a key to "predict" the following word


### Important commands:

#### source ../bin/activate

This starts the virtual environment.

#### gunicorn --bind 0.0.0.0:8080 app:app &
Runs the gunicorn server
Needs to be run whenever app.py changes
#### sudo nano /etc/nginx/nginx.conf
Edits the nginx config file
#### sudo service nginx start
#### sudo service nginx stop
Needs to be run whenever the conf file changes

#### ps ax|grep gunicorn
Lists the gunicorn processes
#### kill <process_id>
Shuts down the gunicorn server

### Languages & tools
Python flask, HTML, CSS, Bootstrap, JavaScript, jQuery, SQLite
