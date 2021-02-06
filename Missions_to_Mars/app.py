from flask import Flask, render_template
import pymongo
import flask_pymongo
import scrape_mars
import re

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

@app.route("/")
def index():
    mars_info = db.collection.find_one()
    return render_template("index.html", info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = db.mars_info
    mars_data = scrape_mars.scrape()
    db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
