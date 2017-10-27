### Important files:

#### app.py
This is the file that runs the server

#### templates/index.html
#### static/css/style.css
#### static/js/script.js

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
