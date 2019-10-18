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
    return render_template("index.html", mars_news=mars_scrape['mars_news'], mars_paragraph=mars_scrape['mars_paragraph'], mars_image=mars_scrape['mars_image'], mars_weather=mars_scrape['mars_weather'], mars_facts=mars_scrape['mars_facts'], img_url1=mars_scrape['mars_hemisphere1'], img_url2=mars_scrape['mars_hemisphere2'], img_url3=mars_scrape['mars_hemisphere3'], img_url4=mars_scrape['mars_hemisphere4'])

@app.route("/scrape")     
def scraper():
    marsy = mycol
    mars_scrape = scrape_mars.scrape()
    marsy.update({}, mars_scrape, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

# Housekeeping codes Test to confirm_
#checkdata = mycol.find() 
#for record in checkdata: 
#    print(record)