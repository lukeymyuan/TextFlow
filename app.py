from flask import Flask, render_template, url_for, redirect
import db
app = Flask(__name__)

@app.route("/")
def home():
        data = db.execute("SELECT * from document")
        print(data)
	return render_template("index.html", data=data)


if __name__ == "__main__":
	app.run(host='0.0.0.0')
