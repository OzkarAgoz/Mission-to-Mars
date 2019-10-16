from flask import Flask, render_template, redirect
import pymongo 
#from pymongo import MongoClient
#from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/")
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mars_db"]
mycol = mydb["mars"]
# client = MongoClient()
# client = MongoClient('localhost', 27017)
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")
# db = client.mars_db
# collection = db.mars

@app.route("/")
def index():
    mars_scrape = mycol.find_one()
    return render_template("index.html", mars_scrape=mars_scrape)

@app.route("/scrape")     
def scraper():
    mars = mycol
    mars_scrape = scrape_mars.scrape()
    mars.update({}, mars_scrape, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=False)