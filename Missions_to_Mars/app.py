from flask import Flask, render_template, redirect
import pymongo
import flask_pymongo
from flask_pymongo import PyMongo
import scrape_mars
import re

app = Flask(__name__)

# Create connection variable
#conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
#db = client.mars_db
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def index():
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", info=mars_info)


@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
