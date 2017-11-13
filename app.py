from flask import Flask, render_template, url_for, redirect, request
import db
import os.path

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

SOURCES = ["*", "Books", "Papers", "Twitter", "Facebook", "RedditSubmission"]
@app.route("/query_db", methods=["POST"])
def handle_query():
    print(request.form)
    source = SOURCES[int(request.form['source'])]
    author = request.form['author']
    filters = []
    if author != '':
        filters.append('author="{0}"'.format(author))
    query = """
    SELECT text FROM {0}
    """.format(source)
    if filters:
        query+="WHERE "+",".join(filters) 
    print(query)

    result = db.execute(query)
    print(result)
    return "goodbye"

if __name__ == "__main__":
	app.run(host='0.0.0.0')
