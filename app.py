from flask import Flask, render_template, redirect
import pymongo 
from pymongo import MongoClient
import scrape_mars

try: 
    conn = MongoClient("mongodb://localhost:27017/") 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB") 

mydb = conn["mars_db"]
mycol = mydb["mars"]

app = Flask(__name__)

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

# Housekeeping codes Test to confirm_
#checkdata = mycol.find() 
#for record in checkdata: 
#    print(record)